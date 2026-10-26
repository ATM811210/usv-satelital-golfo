import sys
from pathlib import Path
import pytest

EDGE_PATH = Path(__file__).resolve().parent.parent / "plataforma_web_gis" / "usv_edge_jetson"
sys.path.insert(0, str(EDGE_PATH))

from edge_vision_fusion import (
    EdgeVisionFusionEngine,
    DetectedObstacle,
    CollisionRisk,
    BiomassDensityClass,
)


@pytest.fixture
def fusion_engine():
    return EdgeVisionFusionEngine(safe_ttc_seconds=18.0)


def test_collision_risk_critical_evasion_on_close_panga(fusion_engine):
    """Detecta panga sin luces a 20 metros y detona evasión crítica de inmediato."""
    obstacles = [
        DetectedObstacle(
            label="panga_sin_luz",
            confidence=0.88,
            bearing_deg=5.0,
            distance_m=20.0,
            relative_speed_knots=4.0,
        )
    ]
    risk, critical_obs = fusion_engine.evaluate_collision_risk(obstacles, own_speed_knots=5.0)
    assert risk == CollisionRisk.CRITICAL_EVASION
    assert critical_obs is not None
    assert critical_obs.label == "panga_sin_luz"


def test_collision_risk_low_confidence_filtered(fusion_engine):
    """Ignora falsos positivos con confianza por debajo del umbral del 45%."""
    low_conf_obstacles = [
        DetectedObstacle(
            label="escombro_flotante",
            confidence=0.30,
            bearing_deg=-15.0,
            distance_m=15.0,
            relative_speed_knots=0.0,
        )
    ]
    risk, critical_obs = fusion_engine.evaluate_collision_risk(low_conf_obstacles, own_speed_knots=5.0)
    assert risk == CollisionRisk.NONE
    assert critical_obs is None


def test_biomass_estimation_rocky_ground_rejection(fusion_engine):
    """Rechaza sustrato rocoso (>2.4 kHz en hidrófono) protegiendo las redes."""
    estimate = fusion_engine.estimate_shrimp_biomass(
        echo_db=-38.0,
        depth_brazas=5.0,
        hydrophone_freq_khz=2.8,  # Firma de arrecife / piedra
        bottom_temp_c=26.0,
    )
    assert estimate.shrimp_viable is False
    assert estimate.density_class == BiomassDensityClass.NULA
    assert estimate.estimated_kg_per_hectare == 0.0


def test_biomass_estimation_high_yield_commercial_shrimp(fusion_engine):
    """Estima alta concentración de zafra en fondo de lodo a 6 brazas."""
    estimate = fusion_engine.estimate_shrimp_biomass(
        echo_db=-38.0,
        depth_brazas=6.0,
        hydrophone_freq_khz=0.8,  # Libre de roca
        bottom_temp_c=26.5,
    )
    assert estimate.shrimp_viable is True
    assert estimate.density_class == BiomassDensityClass.ALTA_CONCENTRACION_ZAFRA
    assert estimate.estimated_kg_per_hectare > 200.0
    assert estimate.depth_m == round(6.0 * 1.8288, 2)
