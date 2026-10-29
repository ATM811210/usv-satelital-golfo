"""
Motor Matemático de Fusión Satelital y Acústica Tri-Especie (Camarón, Pescado y Jaiba)
Soporta dos arquitecturas de instrumentación:
  1. MVP_BAJO_COSTO: PlanetScope Trial / Sentinel-2 + Garmin CHIRP 50/200kHz + Side-Scan GT56UHD (455/800kHz) + Atlas EZO-DO + Turner Cyclops-7F + Aquarian H3d.
  2. GRADO_CIENTIFICO: PlanetScope SuperDove 8B + SAR + Simrad EK80 WBT Mini (70/120/200/333kHz) + Oculus M1200d + RBRconcerto³ CTD-DO + icListen HF.

Opciones de Análisis Satelital + In-Situ:
  - Opción 1 (CAMARON): Camarón Azul/Café (L. stylirostris / F. californiensis) en 2.0 a 12.5 brazas.
  - Opción 2 (PESCADO): Sardina Monterrey, Curvina, Pargo y Escama en frentes de Clorofila-a (10 a 90 brazas).
  - Opción 3 (JAIBA): Jaiba Café/Guerrera (C. bellicosus) y Jaiba Azul (C. arcuatus) en 0.8 a 8.5 brazas con filtro anti-hipoxia DO y Side-Scan.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime


SENSOR_TIERS: Dict[str, Dict[str, Any]] = {
    "ETAPA_1_SATELITAL": {
        "tier_id": "ETAPA_1_SATELITAL",
        "nombre": "Etapa 1 (Día 21): Solo Análisis Satelital 3m Tri-Especie + App Capitán (Sin USV)",
        "inversion_total_llave_en_mano_usd": 11120,
        "costo_datos_satelitales_6m_usd": 4320,
        "costo_materiales_navales_usd": 0,
        "costo_sensores_usd": 0,
        "mano_obra_astillero_usd": 0,
        "mano_obra_ingenieria_software_usd": 6800,
        "starlink_incluido": "No requiere USV (Entrega directa a celulares y plotters en muelle)",
        "satelite": "PlanetScope SuperDove 3.0m Diario (8-Bandas, $600/mes) + Sentinel-2 (10m) + VIIRS SST + Copernicus CMEMS (Temp/Salinidad/DO Fondo)",
        "sonar_vertical": "N/A (Fase 1 Satelital Pura)",
        "sonar_jaiba_bento": "Batimetría Digital GEBCO + Reflectancia Turbidez 3m",
        "sonda_quimica_do": "Modelo Biogeoquímico Diario CMEMS (Oxígeno Disuelto y Clorofila-a)",
        "hidrofono": "Carta Histórica de Exclusión de Roca",
        "vision_submarina": "N/A",
        "incertidumbre_biomasa_pct": 22.0,
    },
    "MVP_BAJO_COSTO": {
        "tier_id": "MVP_BAJO_COSTO",
        "nombre": "MVP Comercial Trimarán 48V Completo (Camarón + Pescado + Jaiba)",
        "inversion_total_llave_en_mano_usd": 53949,
        "costo_datos_satelitales_6m_usd": 4320,
        "costo_materiales_navales_usd": 19229,
        "costo_sensores_usd": 10500,
        "mano_obra_astillero_usd": 3500,
        "mano_obra_ingenieria_software_usd": 16400,
        "starlink_incluido": "INDISPENSABLE: Starlink Mini DC ($599) + 6 Meses Roam Marítimo ($900) + Backup RFD900x 915MHz ($250)",
        "satelite": "PlanetScope 3.0m Diario (8-Bandas) + Sentinel-2 (10m) + VIIRS + CMEMS",
        "sonar_vertical": "Garmin GSD 25 + Transductor Bronce Airmar B265LH CHIRP 1kW (50/200 kHz) ($2,600)",
        "sonar_jaiba_bento": "Cerulean Omniscan 450 Side-Scan / Garmin GT56UHD Industrial (455/800/1000 kHz) ($1,850)",
        "sonda_quimica_do": "Turner Cyclops-7F (Clorofila/Turbidez) ($3,200) + Sonda Óptica DO Industrial Sumergible ($950)",
        "hidrofono": "Aquarian H3d-Ethernet Digital ($1,900) — Filtro Roca >2.4kHz y Quelas Jaiba 1.2-3.5kHz",
        "vision_submarina": "FLIR Boson 320 Térmica + Cámara Quilla Low-Light HD en Jetson Orin Nano (67 TOPS)",
        "incertidumbre_biomasa_pct": 11.5,
    },
    "GRADO_CIENTIFICO": {
        "tier_id": "GRADO_CIENTIFICO",
        "nombre": "Grado Científico Trimarán 48V (Certificación INAPESCA / CIBNOR / Exportación)",
        "inversion_total_llave_en_mano_usd": 148400,
        "costo_datos_satelitales_6m_usd": 12600,
        "costo_materiales_navales_usd": 28900,
        "costo_sensores_usd": 78400,
        "mano_obra_astillero_usd": 4500,
        "mano_obra_ingenieria_software_usd": 24000,
        "starlink_incluido": "INDISPENSABLE: Starlink Flat High Performance Marítimo + 6 Meses Prioridad Oceánica + RFD900x",
        "satelite": "PlanetScope SuperDove 3.0m 8-Bandas Regional + Radar SAR Capella/ICEYE Todo-Clima + CMEMS",
        "sonar_vertical": "Simrad EK80 WBT Mini Multifrecuencia Banda Ancha (70/120/200/333 kHz) ($24,500)",
        "sonar_jaiba_bento": "Cámara Acústica Multihaz Blueprint Subsea Oculus M1200d (1.2/2.1 MHz) + Edgetech 4125i ($31,500)",
        "sonda_quimica_do": "RBRconcerto³ C.T.D.DO.Chl.Turb (Precisión ±0.002°C, Optodo Rápido O2) ($13,600)",
        "hidrofono": "Ocean Sonics icListen Smart Hydrophone HF (10 Hz - 200 kHz Calibrado) ($8,800)",
        "vision_submarina": "Sistema Estéreo SubC Imaging + FLIR Boson 640 Radiométrica (Jetson AGX Orin 275 TOPS)",
        "incertidumbre_biomasa_pct": 3.8,
    },
}


@dataclass
class EnvironmentalCell:
    lat: float
    lon: float
    red_reflectance: float                              # Banda Roja PlanetScope/S2 (665 nm)
    green_reflectance: float                            # Banda Verde PlanetScope/S2 (565 nm)
    red_edge_reflectance: float                         # Banda RedEdge PlanetScope/S2 (705 nm)
    sst_night_c: float                                  # Temperatura superficial VIIRS/GOES (°C)
    bottom_temp_c: float                                # Temperatura de fondo CMEMS / CTD (°C)
    salinity_psu: float                                 # Salinidad de fondo CMEMS / CTD (PSU)
    depth_brazas: float                                 # Profundidad en brazas (1 braza = 1.8288 m)
    tide_speed_knots: float                             # Velocidad de corriente de marea (nudos)
    usv_confirmed: bool = False
    hydrophone_rock_hazard: bool = False
    dissolved_oxygen_mg_l: float = 5.4                  # Oxígeno disuelto de fondo (DO mg/L)
    sidescan_substrate: str = "ECOTONO_ARENA_CONCHAL"   # LODO_ORGANICO, ECOTONO_ARENA_CONCHAL, ZOSTERA_PASTO, ROCA_DURA
    hydrophone_jaiba_foraging: bool = False             # Estridulación/trituración de bivalvos (1.2 - 3.5 kHz)
    sensor_tier: str = "MVP_BAJO_COSTO"                 # MVP_BAJO_COSTO | GRADO_CIENTIFICO


def get_sensor_tier_profile(tier: str = "MVP_BAJO_COSTO") -> Dict[str, Any]:
    """Devuelve las especificaciones de instrumentación del tier seleccionado."""
    return SENSOR_TIERS.get(tier.upper(), SENSOR_TIERS["MVP_BAJO_COSTO"])


def compute_ndti(red: float, green: float) -> float:
    """Índice Diferencial Normalizado de Turbidez (PlanetScope 3m / Sentinel-2 10m)."""
    denom = red + green
    if denom <= 1e-6:
        return 0.0
    return round((red - green) / denom, 4)


def compute_ndci_chlorophyll(red_edge: float, red: float) -> float:
    """
    Índice Diferencial Normalizado de Clorofila-a (NDCI) usando banda RedEdge (705 nm)
    + calibración in-situ con fluorómetro (Turner Cyclops-7F o RBRconcerto³).
    """
    denom = red_edge + red
    if denom <= 1e-6:
        return 0.5
    ndci = (red_edge - red) / denom
    chl_mg_m3 = max(0.1, round(1.8 + 14.5 * ndci + 28.0 * (ndci ** 2), 2))
    return chl_mg_m3


def score_shrimp_night_hsi(cell: EnvironmentalCell) -> Dict[str, Any]:
    """
    OPCIÓN 1 — CAMARÓN (Nocturno):
    Calcula el Índice de Idoneidad de Hábitat para Camarón Azul/Café (0 - 100):
      - 35% Gradiente de Turbidez Óptica (NDTI óptimo: 0.06 a 0.22)
      - 25% Ventana Termohalina de Fondo (24.0°C - 28.5°C y 28 - 36 PSU)
      - 20% Batimetría Somera de Canal/Bahía (2.0 a 12.0 brazas)
      - 20% Corriente de Marea de Reflujo (1.2 a 3.8 nudos)
      - Penalización por hipoxia (<2.2 mg/L) o roca rompe-redes (>2.4 kHz).
    """
    ndti = compute_ndti(cell.red_reflectance, cell.green_reflectance)

    if 0.06 <= ndti <= 0.22:
        s_turb = 100.0 - abs(ndti - 0.14) * 250.0
    elif 0.02 <= ndti < 0.06:
        s_turb = 60.0
    else:
        s_turb = 25.0

    if 24.0 <= cell.bottom_temp_c <= 28.5:
        s_temp = 100.0 - abs(cell.bottom_temp_c - 26.2) * 8.0
    else:
        s_temp = max(10.0, 100.0 - abs(cell.bottom_temp_c - 26.2) * 18.0)

    if 28.0 <= cell.salinity_psu <= 36.0:
        s_sal = 100.0
    else:
        s_sal = max(20.0, 100.0 - abs(cell.salinity_psu - 33.5) * 12.0)
    s_thermohaline = 0.65 * s_temp + 0.35 * s_sal

    if 2.0 <= cell.depth_brazas <= 12.0:
        s_depth = 100.0
    elif 12.0 < cell.depth_brazas <= 16.0:
        s_depth = 65.0
    else:
        s_depth = 15.0

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

    if cell.dissolved_oxygen_mg_l < 2.2:
        raw_hsi = min(raw_hsi, 25.0)
    elif cell.hydrophone_rock_hazard:
        raw_hsi = min(raw_hsi, 35.0)
    elif cell.usv_confirmed:
        bonus = 9.0 if cell.sensor_tier == "GRADO_CIENTIFICO" else 7.5
        raw_hsi = min(99.4, raw_hsi + bonus)

    return {
        "especie_analizada": "CAMARON",
        "score_hsi": round(raw_hsi, 1),
        "ndti_3m": ndti,
        "clorofila_mg_m3": compute_ndci_chlorophyll(cell.red_edge_reflectance, cell.red_reflectance),
        "oxigeno_disuelto_mg_l": cell.dissolved_oxygen_mg_l,
        "sensor_tier": cell.sensor_tier,
        "prioridad": 1 if raw_hsi >= 85.0 else (2 if raw_hsi >= 70.0 else 3),
    }


def score_sardine_day_hsi(cell: EnvironmentalCell) -> Dict[str, Any]:
    """
    OPCIÓN 2 — PESCADO / PELÁGICOS Y ESCAMA (Diurno):
    Calcula el Índice de Idoneidad para Sardina Monterrey, Curvina, Pargo y Escama:
      - 45% Frentes de Clorofila-a RedEdge (>2.2 mg/m³)
      - 35% Gradiente Térmico Pelágico (17.5°C - 23.0°C)
      - 20% Batimetría de Talud y Canal Exterior (10 a 90 brazas)
    """
    chl = compute_ndci_chlorophyll(cell.red_edge_reflectance, cell.red_reflectance)
    ndti = compute_ndti(cell.red_reflectance, cell.green_reflectance)

    if chl >= 2.5:
        s_chl = min(100.0, 80.0 + (chl - 2.5) * 8.0)
    elif 1.2 <= chl < 2.5:
        s_chl = 65.0
    else:
        s_chl = 25.0

    if 17.5 <= cell.sst_night_c <= 23.0:
        s_sst = 95.0
    else:
        s_sst = max(25.0, 95.0 - abs(cell.sst_night_c - 20.5) * 10.0)

    s_depth = 95.0 if 10.0 <= cell.depth_brazas <= 90.0 else 45.0

    raw_hsi = 0.45 * s_chl + 0.35 * s_sst + 0.20 * s_depth
    if cell.usv_confirmed:
        bonus = 7.5 if cell.sensor_tier == "GRADO_CIENTIFICO" else 6.0
        raw_hsi = min(98.8, raw_hsi + bonus)

    return {
        "especie_analizada": "PESCADO",
        "score_hsi": round(raw_hsi, 1),
        "ndti_3m": ndti,
        "clorofila_mg_m3": chl,
        "oxigeno_disuelto_mg_l": cell.dissolved_oxygen_mg_l,
        "sensor_tier": cell.sensor_tier,
        "prioridad": 1 if raw_hsi >= 85.0 else (2 if raw_hsi >= 70.0 else 3),
    }


def score_crab_jaiba_hsi(cell: EnvironmentalCell) -> Dict[str, Any]:
    """
    OPCIÓN 3 — JAIBA BENTÓNICA (Callinectes bellicosus / Callinectes arcuatus):
    Evalúa hábitat para calado de trampas/nasas jaiberas combinando satélite + Side-Scan + Sonda DO:
      - 30% Oxígeno Disuelto en Fondo (DO >= 3.2 mg/L óptimo; si < 2.2 mg/L descarta por mortandad en trampa)
      - 25% Sustrato Acústico Side-Scan (455/800 kHz o Oculus 1.2MHz): Ecótono Arena-Conchal / Zostera / Lodo firme
      - 20% Batimetría Somera Estuarina/Costera (0.8 a 8.5 brazas)
      - 15% Ventana Termohalina Bentónica (22.0°C - 30.0°C; <17.5°C letargo invernal; 16 - 38 PSU)
      - 10% Turbidez Moderada de Estero (NDTI 0.04 a 0.18)
      - Bonificación por detección hidrofónica de forrajeo (trituración de bivalvos en 1.2 - 3.5 kHz).
    """
    ndti = compute_ndti(cell.red_reflectance, cell.green_reflectance)
    chl = compute_ndci_chlorophyll(cell.red_edge_reflectance, cell.red_reflectance)

    # 1. Filtro Crítico de Hipoxia en Fondo (Sonda Óptica DO)
    if cell.dissolved_oxygen_mg_l < 2.2:
        return {
            "especie_analizada": "JAIBA",
            "score_hsi": 12.0,
            "ndti_3m": ndti,
            "clorofila_mg_m3": chl,
            "oxigeno_disuelto_mg_l": cell.dissolved_oxygen_mg_l,
            "sustrato_sidescan": cell.sidescan_substrate,
            "alerta_hipoxia_trampas": True,
            "densidad_trampas_sugerida_ha": 0,
            "sensor_tier": cell.sensor_tier,
            "prioridad": 3,
        }

    if cell.dissolved_oxygen_mg_l >= 4.0:
        s_do = 100.0
    elif 3.0 <= cell.dissolved_oxygen_mg_l < 4.0:
        s_do = 85.0
    else:
        s_do = 50.0

    # 2. Score Sustrato Side-Scan (455/800 kHz o Cámara Acústica Oculus)
    substrate_scores = {
        "ECOTONO_ARENA_CONCHAL": 100.0,
        "ZOSTERA_PASTO": 95.0,
        "LODO_ORGANICO": 82.0,
        "ARENA_FIRME": 75.0,
        "ROCA_DURA": 30.0,
    }
    s_substrate = substrate_scores.get(cell.sidescan_substrate, 75.0)

    # 3. Score Batimetría Jaibera (0.8 a 8.5 brazas)
    if 0.8 <= cell.depth_brazas <= 8.5:
        s_depth = 100.0
    elif 8.5 < cell.depth_brazas <= 12.0:
        s_depth = 60.0
    else:
        s_depth = 15.0

    # 4. Score Termohalino (C. bellicosus 28-38 PSU / C. arcuatus 16-34 PSU; Temp 22-30°C)
    if 22.0 <= cell.bottom_temp_c <= 30.0:
        s_temp = 98.0
    elif 18.0 <= cell.bottom_temp_c < 22.0:
        s_temp = 65.0
    else:
        s_temp = 20.0  # Letargo térmico invernal (se entierra y no entra a la nasa)

    s_sal = 98.0 if 16.0 <= cell.salinity_psu <= 38.5 else 45.0
    s_thermo = 0.65 * s_temp + 0.35 * s_sal

    # 5. Score Turbidez Estuarina
    s_turb = 95.0 if 0.04 <= ndti <= 0.19 else 60.0

    raw_hsi = (
        0.30 * s_do
        + 0.25 * s_substrate
        + 0.20 * s_depth
        + 0.15 * s_thermo
        + 0.10 * s_turb
    )

    # Bonificación por acústica pasiva (quelas triturando almejas/bivalvos) y confirmación USV
    if cell.hydrophone_jaiba_foraging:
        raw_hsi = min(99.5, raw_hsi + 5.5)
    if cell.usv_confirmed:
        bonus = 5.0 if cell.sensor_tier == "GRADO_CIENTIFICO" else 3.5
        raw_hsi = min(99.6, raw_hsi + bonus)

    score_final = round(raw_hsi, 1)
    trampas_ha = 25 if score_final >= 85.0 else (15 if score_final >= 70.0 else 0)

    return {
        "especie_analizada": "JAIBA",
        "score_hsi": score_final,
        "ndti_3m": ndti,
        "clorofila_mg_m3": chl,
        "oxigeno_disuelto_mg_l": cell.dissolved_oxygen_mg_l,
        "sustrato_sidescan": cell.sidescan_substrate,
        "alerta_hipoxia_trampas": False,
        "densidad_trampas_sugerida_ha": trampas_ha,
        "sensor_tier": cell.sensor_tier,
        "prioridad": 1 if score_final >= 85.0 else (2 if score_final >= 70.0 else 3),
    }


def analyze_species_hsi(
    cell: EnvironmentalCell,
    especie_opcion: str = "CAMARON",
) -> Dict[str, Any]:
    """
    Enrutador unificado para las 3 opciones de análisis satelital + USV:
      - 'CAMARON' (o 'NOCTURNO_CAMARON')
      - 'PESCADO' (o 'DIURNO_SARDINA' / 'DIURNO_PESCADO')
      - 'JAIBA'   (o 'PROSPECCION_JAIBA')
    """
    key = especie_opcion.upper()
    if "JAIBA" in key or "CRAB" in key:
        return score_crab_jaiba_hsi(cell)
    if "PESCADO" in key or "SARDINA" in key or "ESCAMA" in key or "DIURNO" in key:
        return score_sardine_day_hsi(cell)
    return score_shrimp_night_hsi(cell)


def export_polygons_to_kml(polygons: List[Dict[str, Any]], turno: str) -> str:
    """
    Genera archivo KML estándar compatible con plotters marinos Garmin, Simrad, Raymarine,
    Navionics y Google Earth móvil para los 3 modos (Camarón, Pescado y Jaiba).
    """
    placemarks = []
    for p in polygons:
        coords_ring = p["geometry"]["coordinates"][0]
        coord_str = " ".join([f"{pt[0]},{pt[1]},0" for pt in coords_ring])
        color_kml = "7d0000ff" if p["properties"]["prioridad"] == 1 else "7d00a5ff"
        if p["properties"].get("riesgo_roca_hidrofono"):
            color_kml = "99ff00ff"

        do_val = p["properties"].get("oxigeno_disuelto_mg_l", 5.2)
        sustrato = p["properties"].get("sustrato_sidescan", "Lodo/Arena")

        placemarks.append(f"""
    <Placemark>
      <name>[{p["properties"]["codigo_zona"]}] {p["properties"]["nombre_canal"]} (HSI: {p["properties"]["score_hsi"]}%)</name>
      <description><![CDATA[
        <b>Especie:</b> {p["properties"]["especie_objetivo"]}<br/>
        <b>Profundidad:</b> {p["properties"]["profundidad_brazas_min"]} - {p["properties"]["profundidad_brazas_max"]} brazas<br/>
        <b>Temp. Fondo (CTD/CMEMS):</b> {p["properties"]["temp_fondo_centigrados"]} °C<br/>
        <b>Salinidad:</b> {p["properties"]["salinidad_psu"]} PSU<br/>
        <b>Oxígeno Disuelto Fondo (DO):</b> {do_val} mg/L<br/>
        <b>Sustrato Side-Scan:</b> {sustrato}<br/>
        <b>Turbidez 3m (NDTI):</b> {p["properties"]["turbidez_ndti"]}<br/>
        <b>Clorofila-a (Turner/RedEdge):</b> {p["properties"]["clorofila_mg_m3"]} mg/m³<br/>
        <b>Verificado por USV Trimarán 48V:</b> {"SÍ (Sonar Confirmado)" if p["properties"]["confirmado_por_usv"] else "Pendiente barrido"}<br/>
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
