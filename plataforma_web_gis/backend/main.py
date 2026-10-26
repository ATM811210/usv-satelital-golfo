"""
API Backend (FastAPI): Plataforma Web GIS Satelital 3m (PlanetScope) + USV Trimarán 48V
Sirve:
- Validación de Token por Cooperativa / Flota Sardinera
- Polígonos GeoJSON de 3m para Turno Nocturno (Camarón) y Turno Diurno (Sardina/Escama)
- Descarga directa de archivos .KML y .GPX para Plotters Garmin / Simrad / Lowrance / Navionics
- Estado Astronómico Lunar y Velocidad de Reflujo de Marea en Bocas
- Telemetría en vivo del USV Trimarán Híbrido 48V (Starlink Mini Webhook)
- Reporte de capturas de capitanes (Online + Sincronización diferida Offline)
"""

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from engine_hsi import export_polygons_to_kml
from gpx_kml_exporter import export_to_marine_gpx
from tide_and_moon import calculate_lunar_and_tidal_state
from satellite_connectors import (
    PlanetScope3mConnector,
    AOI_BOXES,
    get_daily_polygons_dataset,
    get_usv_live_telemetry,
)

app = FastAPI(
    title="API Satelital 3m (PlanetScope) + USV Trimarán 48V Stealth",
    version="2.0.0",
    description="Motor Geoespacial Doble Turno: Camarón (Noche) + Sardina/Curvina/Aguamala (Día)",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VALID_TOKENS = {
    "TOPO-2026-VIP-TOKEN": {
        "cooperativa": "Alianza Cooperativa Topolobampo - Ohuira",
        "zona": "Topolobampo-Ohuira",
        "plan": "MULTI-ESPECIE 24H (Camarón + Sardina/Escama)",
        "activa": True,
    },
    "SARDINA-2026-DAY-TOKEN": {
        "cooperativa": "Flota Sardinera y Escamera del Pacífico",
        "zona": "Topolobampo-Ohuira",
        "plan": "TURNO DIURNO (Sardina / Curvina / Clorofila-a)",
        "activa": True,
    },
    "KINO-2026-VIP-TOKEN": {
        "cooperativa": "Sociedad Cooperativa Bahía de Kino",
        "zona": "Bahia de Kino",
        "plan": "MULTI-ESPECIE 24H (Camarón + Sardina/Aguamala)",
        "activa": True,
    },
}

CAPTURAS_MEMORIA: List[Dict[str, Any]] = [
    {
        "id": "cap-001",
        "fecha": "2026-10-18 06:10",
        "embarcacion": "Panga La Reina del Maviri II",
        "zona": "TOPO-N1 (Canal Las Copas)",
        "especie": "Camarón Azul Grande (U15)",
        "kilos": 94.5,
        "gasolina_ahorrada_l": 35.0,
        "comentario": "Llegamos directo al punto confirmado por el USV a 4.5 brazas, cero piedra.",
    },
    {
        "id": "cap-002",
        "fecha": "2026-10-18 11:20",
        "embarcacion": "B/M Don Ernesto (Sardinero)",
        "zona": "TOPO-D1 (Talud Farallón)",
        "especie": "Sardina Monterrey",
        "kilos": 42000.0,
        "gasolina_ahorrada_l": 450.0,
        "comentario": "Mancha exacta donde el sensor de Clorofila-a marcó 5.1 mg/m³ a 28 brazas.",
    },
]


class CaptureReportInput(BaseModel):
    embarcacion: str
    codigo_zona: str
    especie: str
    kilos: float
    gasolina_ahorrada_l: Optional[float] = 30.0
    comentario: Optional[str] = ""


@app.get("/api/v1/status")
def system_status():
    ps = PlanetScope3mConnector()
    return {
        "status": "OPERATIVO",
        "hito_actual": "Hito 1 (Día 21) — Plataforma Satelital 3m + App Panga Offline + Telemetría USV 48V",
        "planetscope": ps.get_status(),
        "zonas_disponibles": AOI_BOXES,
    }


@app.get("/api/v1/astronomy-tides")
def astronomy_and_tides(zona: str = Query("Topolobampo-Ohuira")):
    return calculate_lunar_and_tidal_state(zona=zona)


@app.get("/api/v1/verify-token")
def verify_token(token: str = Query("TOPO-2026-VIP-TOKEN")):
    info = VALID_TOKENS.get(token)
    if not info or not info["activa"]:
        raise HTTPException(
            status_code=403,
            detail="Token de cooperativa vencido o inválido. Contacte al administrador para renovar su suscripción mensual.",
        )
    return {"valid": True, "cliente": info}


@app.get("/api/v1/polygons")
def get_polygons(
    zona: str = Query("Topolobampo-Ohuira"),
    turno: str = Query("NOCTURNO_CAMARON"),
    token: str = Query("TOPO-2026-VIP-TOKEN"),
):
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=403, detail="Acceso bloqueado: Token inválido.")
    return get_daily_polygons_dataset(zona=zona, turno=turno)


@app.get("/api/v1/export.kml")
def download_kml(
    zona: str = Query("Topolobampo-Ohuira"),
    turno: str = Query("NOCTURNO_CAMARON"),
):
    dataset = get_daily_polygons_dataset(zona=zona, turno=turno)
    kml_content = export_polygons_to_kml(dataset["features"], turno=turno)
    filename = f"boletin_{zona.lower().replace(' ', '_')}_{turno.lower()}.kml"
    return Response(
        content=kml_content,
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/v1/export.gpx")
def download_gpx(
    zona: str = Query("Topolobampo-Ohuira"),
    turno: str = Query("NOCTURNO_CAMARON"),
):
    dataset = get_daily_polygons_dataset(zona=zona, turno=turno)
    telemetry = get_usv_live_telemetry(zona=zona, turno=turno)
    gpx_content = export_to_marine_gpx(
        polygons=dataset["features"],
        usv_track=telemetry["track_coordinates"],
        zona=zona,
        turno=turno,
    )
    filename = f"plotter_{zona.lower().replace(' ', '_')}_{turno.lower()}.gpx"
    return Response(
        content=gpx_content,
        media_type="application/gpx+xml",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/api/v1/usv-telemetry")
def usv_telemetry(
    zona: str = Query("Topolobampo-Ohuira"),
    turno: str = Query("NOCTURNO_CAMARON"),
):
    return get_usv_live_telemetry(zona=zona, turno=turno)


@app.get("/api/v1/captures")
def list_captures():
    return {"capturas": CAPTURAS_MEMORIA}


@app.post("/api/v1/captures")
def create_capture(report: CaptureReportInput):
    entry = {
        "id": f"cap-{len(CAPTURAS_MEMORIA) + 1:03d}",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "embarcacion": report.embarcacion,
        "zona": report.codigo_zona,
        "especie": report.especie,
        "kilos": report.kilos,
        "gasolina_ahorrada_l": report.gasolina_ahorrada_l,
        "comentario": report.comentario,
    }
    CAPTURAS_MEMORIA.insert(0, entry)
    return {"ok": True, "registro": entry}
