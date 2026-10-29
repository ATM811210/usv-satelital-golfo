import sys
from pathlib import Path
import pytest

BACKEND_PATH = Path(__file__).resolve().parent.parent / "plataforma_web_gis" / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from engine_hsi import (
    EnvironmentalCell,
    get_sensor_tier_profile,
    analyze_species_hsi,
    score_crab_jaiba_hsi,
)


def test_dual_tier_sensor_profiles():
    """Valida que existan el MVP de Bajo Costo y la configuración de Grado Científico."""
    mvp = get_sensor_tier_profile("MVP_BAJO_COSTO")
    sci = get_sensor_tier_profile("GRADO_CIENTIFICO")

    assert mvp["costo_sensores_usd"] < 10000
    assert "GT56UHD" in mvp["sonar_jaiba_bento"]
    assert sci["costo_sensores_usd"] > 50000
    assert "Simrad EK80" in sci["sonar_vertical"]
    assert sci["incertidumbre_biomasa_pct"] < mvp["incertidumbre_biomasa_pct"]


def test_three_species_satellite_options_router():
    """Valida el análisis satelital + in-situ para las 3 opciones: CAMARON, PESCADO y JAIBA."""
    cell_camaron = EnvironmentalCell(
        lat=25.58,
        lon=-109.06,
        red_reflectance=0.14,
        green_reflectance=0.10,
        red_edge_reflectance=0.16,
        sst_night_c=26.5,
        bottom_temp_c=26.2,
        salinity_psu=34.0,
        depth_brazas=5.5,
        tide_speed_knots=2.1,
        usv_confirmed=True,
        dissolved_oxygen_mg_l=5.4,
    )
    res_cam = analyze_species_hsi(cell_camaron, "CAMARON")
    assert res_cam["especie_analizada"] == "CAMARON"
    assert res_cam["score_hsi"] >= 85.0
    assert res_cam["prioridad"] == 1

    cell_pescado = EnvironmentalCell(
        lat=25.48,
        lon=-109.18,
        red_reflectance=0.08,
        green_reflectance=0.09,
        red_edge_reflectance=0.14,
        sst_night_c=20.2,
        bottom_temp_c=19.0,
        salinity_psu=34.8,
        depth_brazas=28.0,
        tide_speed_knots=1.4,
        usv_confirmed=True,
    )
    res_pes = analyze_species_hsi(cell_pescado, "PESCADO")
    assert res_pes["especie_analizada"] == "PESCADO"
    assert res_pes["score_hsi"] >= 85.0

    cell_jaiba = EnvironmentalCell(
        lat=25.61,
        lon=-109.02,
        red_reflectance=0.12,
        green_reflectance=0.09,
        red_edge_reflectance=0.13,
        sst_night_c=25.8,
        bottom_temp_c=25.5,
        salinity_psu=32.5,
        depth_brazas=3.2,
        tide_speed_knots=1.5,
        usv_confirmed=True,
        dissolved_oxygen_mg_l=5.1,
        sidescan_substrate="ECOTONO_ARENA_CONCHAL",
        hydrophone_jaiba_foraging=True,
        sensor_tier="GRADO_CIENTIFICO",
    )
    res_jai = analyze_species_hsi(cell_jaiba, "JAIBA")
    assert res_jai["especie_analizada"] == "JAIBA"
    assert res_jai["score_hsi"] >= 90.0
    assert res_jai["densidad_trampas_sugerida_ha"] == 25
    assert res_jai["alerta_hipoxia_trampas"] is False


def test_jaiba_hypoxia_trap_mortality_protection():
    """Bloquea el calado de trampas jaiberas cuando el sensor DO detecta hipoxia (<2.2 mg/L)."""
    hypoxic_cell = EnvironmentalCell(
        lat=25.62,
        lon=-109.01,
        red_reflectance=0.12,
        green_reflectance=0.09,
        red_edge_reflectance=0.13,
        sst_night_c=27.0,
        bottom_temp_c=27.0,
        salinity_psu=30.0,
        depth_brazas=2.5,
        tide_speed_knots=0.4,
        dissolved_oxygen_mg_l=1.6,  # Hipoxia severa de estero
        sidescan_substrate="ECOTONO_ARENA_CONCHAL",
    )
    res = score_crab_jaiba_hsi(hypoxic_cell)
    assert res["alerta_hipoxia_trampas"] is True
    assert res["densidad_trampas_sugerida_ha"] == 0
    assert res["prioridad"] == 3
