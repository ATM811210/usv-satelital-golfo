"""
Motor Matemático de Fusión Satelital y Acústica (HSI Multi-Especie Doble Turno)
- Turno Nocturno (22:00 hrs): Camarón Azul/Café (L. stylirostris / F. californiensis) en 2 a 12 brazas.
- Turno Diurno (05:00 hrs): Sardina Monterrey, Curvina, Pargo y Aguamala en frentes de Clorofila-a.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import math
from datetime import datetime


@dataclass
class EnvironmentalCell:
    lat: float
    lon: float
    red_reflectance: float       # Banda Roja PlanetScope (665 nm) a 3m
    green_reflectance: float     # Banda Verde PlanetScope (565 nm) a 3m
    red_edge_reflectance: float  # Banda RedEdge PlanetScope (705 nm) a 3m
    sst_night_c: float           # Temperatura superficial nocturna VIIRS/GOES (°C)
    bottom_temp_c: float         # Temperatura potencial de fondo CMEMS / CTD (°C)
    salinity_psu: float          # Salinidad de fondo CMEMS / CTD (PSU)
    depth_brazas: float          # Profundidad en brazas (1 braza = 1.8288 m)
    tide_speed_knots: float      # Velocidad de reflujo de marea (nudos)
    usv_confirmed: bool = False
    hydrophone_rock_hazard: bool = False


def compute_ndti(red: float, green: float) -> float:
    """Índice Diferencial Normalizado de Turbidez (PlanetScope 3m)."""
    denom = red + green
    if denom <= 1e-6:
        return 0.0
    return round((red - green) / denom, 4)


def compute_ndci_chlorophyll(red_edge: float, red: float) -> float:
    """
    Índice Diferencial Normalizado de Clorofila-a (NDCI) usando banda RedEdge (705 nm)
    de PlanetScope 8-bandas + calibración con sonda Turner Cyclops-7F.
    """
    denom = red_edge + red
    if denom <= 1e-6:
        return 0.5
    ndci = (red_edge - red) / denom
    # Conversión empírica a mg/m³ para aguas costeras del Golfo de California
    chl_mg_m3 = max(0.1, round(1.8 + 14.5 * ndci + 28.0 * (ndci ** 2), 2))
    return chl_mg_m3


def score_shrimp_night_hsi(cell: EnvironmentalCell) -> Dict[str, Any]:
    """
    Calcula el Índice de Idoneidad de Hábitat Nocturno para Camarón (0 - 100):
    Pesos:
      - 35% Gradiente de Turbidez Óptica PlanetScope 3m (NDTI óptimo: 0.06 a 0.22)
      - 25% Ventana Termohalina de Fondo (24.0°C - 28.5°C y 28 - 36 PSU)
      - 20% Batimetría Somera de Canal/Bahía (2.0 a 12.0 brazas)
      - 20% Corriente de Marea de Reflujo (1.2 a 3.8 nudos)
    """
    ndti = compute_ndti(cell.red_reflectance, cell.green_reflectance)

    # 1. Score Turbidez (borde de pluma sedimentaria rica en nutrientes)
    if 0.06 <= ndti <= 0.22:
        s_turb = 100.0 - abs(ndti - 0.14) * 250.0
    elif 0.02 <= ndti < 0.06:
        s_turb = 60.0
    else:
        s_turb = 25.0

    # 2. Score Termohalino de Fondo
    if 24.0 <= cell.bottom_temp_c <= 28.5:
        s_temp = 100.0 - abs(cell.bottom_temp_c - 26.2) * 8.0
    else:
        s_temp = max(10.0, 100.0 - abs(cell.bottom_temp_c - 26.2) * 18.0)

    if 28.0 <= cell.salinity_psu <= 36.0:
        s_sal = 100.0
    else:
        s_sal = max(20.0, 100.0 - abs(cell.salinity_psu - 33.5) * 12.0)
    s_thermohaline = 0.65 * s_temp + 0.35 * s_sal

    # 3. Score Batimetría (2 a 12 brazas para pangas y chinchorros)
    if 2.0 <= cell.depth_brazas <= 12.0:
        s_depth = 100.0
    elif 12.0 < cell.depth_brazas <= 16.0:
        s_depth = 65.0
    else:
        s_depth = 15.0

    # 4. Score Dinámica de Marea
    if 1.2 <= cell.tide_speed_knots <= 3.8:
        s_tide = 95.0
    else:
        s_tide = 55.0

    raw_hsi = (
        0.35 * s_turb
        + 0.25 * s_thermohaline
        + 0.20 * s_depth
        + 0.20 * s_tide
    )

    # Bonificación por confirmación acústica del USV (CHIRP 200 kHz) o penalización por roca en hidrófono
    if cell.hydrophone_rock_hazard:
        raw_hsi = min(raw_hsi, 35.0)
    elif cell.usv_confirmed:
        raw_hsi = min(99.4, raw_hsi + 7.5)

    return {
        "score_hsi": round(raw_hsi, 1),
        "ndti_3m": ndti,
        "clorofila_mg_m3": compute_ndci_chlorophyll(cell.red_edge_reflectance, cell.red_reflectance),
        "prioridad": 1 if raw_hsi >= 85.0 else (2 if raw_hsi >= 70.0 else 3),
    }


def score_sardine_day_hsi(cell: EnvironmentalCell) -> Dict[str, Any]:
    """
    Calcula el Índice de Idoneidad Diurno para Sardina Monterrey, Curvina y Aguamala:
    Basado en Frentes de Surgencia Térmica (17.5°C - 22.5°C) + Picos de Clorofila-a (>2.2 mg/m³)
    + Sondeo Acústico Profundo en 50 kHz (12 a 90 brazas).
    """
    chl = compute_ndci_chlorophyll(cell.red_edge_reflectance, cell.red_reflectance)
    ndti = compute_ndti(cell.red_reflectance, cell.green_reflectance)

    # 1. Score Clorofila-a (Fitoplancton para Sardina)
    if chl >= 2.5:
        s_chl = min(100.0, 80.0 + (chl - 2.5) * 8.0)
    elif 1.2 <= chl < 2.5:
        s_chl = 65.0
    else:
        s_chl = 25.0

    # 2. Score Frente Térmico Pelágico
    if 17.5 <= cell.sst_night_c <= 23.0:
        s_sst = 95.0
    else:
        s_sst = max(25.0, 95.0 - abs(cell.sst_night_c - 20.5) * 10.0)

    # 3. Profundidad Exterior (10 a 90 brazas)
    s_depth = 95.0 if 10.0 <= cell.depth_brazas <= 90.0 else 45.0

    raw_hsi = 0.45 * s_chl + 0.35 * s_sst + 0.20 * s_depth
    if cell.usv_confirmed:
        raw_hsi = min(98.8, raw_hsi + 6.0)

    return {
        "score_hsi": round(raw_hsi, 1),
        "ndti_3m": ndti,
        "clorofila_mg_m3": chl,
        "prioridad": 1 if raw_hsi >= 85.0 else (2 if raw_hsi >= 70.0 else 3),
    }


def export_polygons_to_kml(polygons: List[Dict[str, Any]], turno: str) -> str:
    """
    Genera archivo KML estándar compatible con plotters marinos Garmin, Simrad, Raymarine,
    Navionics y Google Earth móvil para envío nocturno (10:00 PM) y diurno (05:00 AM).
    """
    placemarks = []
    for p in polygons:
        coords_ring = p["geometry"]["coordinates"][0]
        coord_str = " ".join([f"{pt[0]},{pt[1]},0" for pt in coords_ring])
        color_kml = "7d0000ff" if p["properties"]["prioridad"] == 1 else "7d00a5ff"
        if p["properties"].get("riesgo_roca_hidrofono"):
            color_kml = "99ff00ff"

        placemarks.append(f"""
    <Placemark>
      <name>[{p["properties"]["codigo_zona"]}] {p["properties"]["nombre_canal"]} (HSI: {p["properties"]["score_hsi"]}%)</name>
      <description><![CDATA[
        <b>Especie:</b> {p["properties"]["especie_objetivo"]}<br/>
        <b>Profundidad:</b> {p["properties"]["profundidad_brazas_min"]} - {p["properties"]["profundidad_brazas_max"]} brazas<br/>
        <b>Temp. Fondo (CTD/CMEMS):</b> {p["properties"]["temp_fondo_centigrados"]} °C<br/>
        <b>Salinidad:</b> {p["properties"]["salinidad_psu"]} PSU<br/>
        <b>Turbidez 3m (NDTI):</b> {p["properties"]["turbidez_ndti"]}<br/>
        <b>Clorofila-a (Turner/RedEdge):</b> {p["properties"]["clorofila_mg_m3"]} mg/m³<br/>
        <b>Verificado por USV Trimarán 48V:</b> {"SÍ (Sonar CHIRP Confirmado)" if p["properties"]["confirmado_por_usv"] else "Pendiente barrido nocturno"}<br/>
        <b>Alerta Hidrófono:</b> {"PELIGRO ROCA ROMPE-REDES (>2kHz)" if p["properties"]["riesgo_roca_hidrofono"] else "Fondo Limpio Lodo/Arena"}<br/>
        <b>Táctica:</b> {p["properties"]["recomendacion_tactica"]}
      ]]></description>
      <Style>
        <LineStyle><color>ff00ffff</color><width>2.5</width></LineStyle>
        <PolyStyle><color>{color_kml}</color></PolyStyle>
      </Style>
      <Polygon>
        <outerBoundaryIs><LinearRing><coordinates>{coord_str}</coordinates></LinearRing></outerBoundaryIs>
      </Polygon>
    </Placemark>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Boletin Satelital 3m + USV 48V ({turno}) - {datetime.utcnow().strftime('%Y-%m-%d')}</name>
    {"".join(placemarks)}
  </Document>
</kml>"""
