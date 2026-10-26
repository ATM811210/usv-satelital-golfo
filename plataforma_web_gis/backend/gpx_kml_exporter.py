"""
ETAPA 3 — Exportador Nativo .GPX (Garmin / Simrad / Lowrance / Furuno)
Genera archivos GPX 1.1 con:
1. <wpt>: Centroides exactos de cada polígono confirmado y alertas de Roca (>2.4 kHz).
2. <rte>: Ruta de navegación segura por el eje del canal dragado verificada por el USV 48V.
3. <trk>: Perímetro de cada polígono de pesca para visualización en pantalla del plotter.
"""

from datetime import datetime
from typing import List, Dict, Any


def export_to_marine_gpx(
    polygons: List[Dict[str, Any]],
    usv_track: List[List[float]],
    zona: str,
    turno: str,
) -> str:
    """
    Construye un archivo GPX 1.1 compatible con todos los plotters marinos comerciales.
    Nota: En GeoJSON las coordenadas vienen como [lon, lat]. En GPX son lat="..." lon="...".
    """
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    wpt_blocks = []
    trk_blocks = []

    for p in polygons:
        props = p["properties"]
        ring = p["geometry"]["coordinates"][0]
        # Calcular centroide del polígono
        lons = [pt[0] for pt in ring[:-1]]
        lats = [pt[1] for pt in ring[:-1]]
        c_lon = round(sum(lons) / len(lons), 5)
        c_lat = round(sum(lats) / len(lats), 5)

        is_rock = props.get("riesgo_roca_hidrofono", False)
        sym = "Skull and Crossbones" if is_rock else ("Fishing Hot Spot Facility" if props["prioridad"] == 1 else "Anchor")
        hsi_label = "PELIGRO ROCA" if is_rock else f"HSI {props['score_hsi']}%"
        name_tag = f"{props['codigo_zona']} {hsi_label}"
        desc_tag = (
            f"{props['nombre_canal']} | {props['especie_objetivo']} | "
            f"{props['profundidad_brazas_min']}-{props['profundidad_brazas_max']} bz | "
            f"Temp Fondo: {props['temp_fondo_centigrados']}C | Clorofila: {props['clorofila_mg_m3']} mg/m3 | "
            f"{props['recomendacion_tactica']}"
        )

        wpt_blocks.append(f"""  <wpt lat="{c_lat}" lon="{c_lon}">
    <time>{now_iso}</time>
    <name>{name_tag}</name>
    <desc>{desc_tag}</desc>
    <sym>{sym}</sym>
  </wpt>""")

        trk_pts = "\n".join([f'      <trkpt lat="{pt[1]}" lon="{pt[0]}"></trkpt>' for pt in ring])
        trk_blocks.append(f"""  <trk>
    <name>POLIGONO {props['codigo_zona']} ({props['nombre_canal']})</name>
    <trkseg>
{trk_pts}
    </trkseg>
  </trk>""")

    # Ruta del canal seguro verificada por el USV Trimarán 48V
    # En satellite_connectors.py, track_coordinates viene como [lon, lat]
    rte_pts = []
    for idx, pt in enumerate(usv_track):
        lon_val, lat_val = pt[0], pt[1]
        rte_pts.append(f"""    <rtept lat="{lat_val}" lon="{lon_val}">
      <name>WP-{idx + 1:02d}-CANAL</name>
      <sym>Navaid, Green</sym>
    </rtept>""")

    rte_block = f"""  <rte>
    <name>RUTA CANAL SEGURO USV 48V ({zona})</name>
{chr(10).join(rte_pts)}
  </rte>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Plataforma Satelital 3m PlanetScope + USV Trimaran 48V Stealth"
  xmlns="http://www.topografix.com/GPX/1/1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata>
    <name>Boletin Pesca Satelital 3m + USV 48V ({zona} - {turno})</name>
    <time>{now_iso}</time>
  </metadata>
{chr(10).join(wpt_blocks)}
{rte_block}
{chr(10).join(trk_blocks)}
</gpx>"""
