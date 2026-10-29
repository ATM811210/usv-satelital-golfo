import sys
from pathlib import Path
import pytest

# Agregar path al controlador edge
EDGE_PATH = Path(__file__).resolve().parent.parent / "plataforma_web_gis" / "usv_edge_jetson"
sys.path.insert(0, str(EDGE_PATH))

from usv_mission_controller import (
    DualF9PMovingBaseline,
    VictronBatteryBank48V,
    USVMissionController48V,
    SubseaSensorFrame,
)


def test_moving_baseline_true_yaw():
    """Valida el cálculo de rumbo verdadero (True Yaw) inmune a EMI de 125A."""
    # Vector hacia el Este puro (rel_north=0, rel_east=2.5) -> 90.0°
    baseline = DualF9PMovingBaseline(
        baseline_length_m=2.5, rel_north_m=0.0, rel_east_m=2.5, rtk_fixed_carrier=True
    )
    assert baseline.compute_true_yaw_deg() == 90.0

    # Vector hacia el Sur puro (rel_north=-2.5, rel_east=0) -> 180.0°
    baseline_south = DualF9PMovingBaseline(
        baseline_length_m=2.5, rel_north_m=-2.5, rel_east_m=0.0, rtk_fixed_carrier=True
    )
    assert baseline_south.compute_true_yaw_deg() == 180.0


def test_victron_battery_limp_home_reserve_floor():
    """Valida que el piso de seguridad del 10% SoC se respete estrictamente."""
    # Batería al 10% exacto -> 0 MN utilizables de Limp-Home
    batt_empty = VictronBatteryBank48V(soc_pct=10.0)
    assert batt_empty.available_limp_home_nm() == 0.0

    # Batería al 86% -> (86 - 10)% de 10240 Wh = 7782.4 Wh -> ~42.1 MN
    batt_nominal = VictronBatteryBank48V(soc_pct=86.0)
    expected_nm = round(7782.4 / 185.0, 1)
    assert batt_nominal.available_limp_home_nm() == expected_nm


def test_failsafe_limp_home_on_generator_fault():
    """Valida el Failsafe de regreso a muelle cuando falla la planta generadora."""
    controller = USVMissionController48V(shift_mode="NOCTURNO_CAMARON")
    controller.generator_fault_flagged = True

    status = controller.evaluate_failsafe_and_power(distance_to_dock_nm=15.0)

    assert status["propulsion_state"] == "LIMP_HOME_EMERGENCY_25NM"
    assert status["target_speed_knots"] == 4.5
    assert status["mavlink_mode"] == "RTL_SAFE_CHANNEL"
    assert controller.generator_4t_running is False


def test_stealth_electric_mode_nocturno_camaron():
    """Valida el sigilo acústico de 0 dB en polígono camaronero nocturno."""
    controller = USVMissionController48V(shift_mode="NOCTURNO_CAMARON")
    controller.battery.soc_pct = 75.0
    controller.generator_fault_flagged = False

    # A 5 MN del muelle con 75% SoC (sobrado de energía)
    status = controller.evaluate_failsafe_and_power(distance_to_dock_nm=5.0)

    assert status["propulsion_state"] == "ELECTRICO_STEALTH_3KT"
    assert status["target_speed_knots"] == 3.0
    assert status["mavlink_mode"] == "AUTO_SWEEP"
    assert "0 dB" in status["generator_4t"]


def test_jaiba_mode_sidescan_and_hypoxia_protection():
    """Valida prospección de Jaiba con Side-Scan 800kHz/Oculus y bloqueo por hipoxia DO."""
    controller = USVMissionController48V(
        shift_mode="PROSPECCION_JAIBA",
        sensor_tier="GRADO_CIENTIFICO",
    )

    # 1. Caso Hipoxia en fondo (<2.2 mg/L) -> Abortar calado de trampas
    hypoxic_frame = SubseaSensorFrame(
        sonar_freq_khz=800,
        depth_brazas=2.5,
        biomass_echo_db=-45.0,
        hydrophone_peak_freq_khz=2.1,
        hydrophone_rms_db=-46.0,
        chlorophyll_a_mg_m3=3.2,
        turbidity_ntu=14.0,
        bottom_temp_c=26.5,
        salinity_psu=31.0,
        dissolved_oxygen_mg_l=1.7,
        sidescan_substrate="ECOTONO_ARENA_CONCHAL",
    )
    res_hyp = controller.analyze_subsea_frame_and_adapt_route(25.61, -109.02, hypoxic_frame)
    assert res_hyp["classification"] == "ZONA_HIPOXICA_MORTALIDAD_TRAMPAS"
    assert res_hyp["action"] == "ABORT_TRAP_DEPLOYMENT_AND_BYPASS"

    # 2. Caso Corredor Jaibero Óptimo -> Trazar línea de trampas
    optimal_frame = SubseaSensorFrame(
        sonar_freq_khz=800,
        depth_brazas=3.2,
        biomass_echo_db=-44.0,
        hydrophone_peak_freq_khz=2.2,
        hydrophone_rms_db=-45.0,
        chlorophyll_a_mg_m3=2.4,
        turbidity_ntu=11.0,
        bottom_temp_c=26.0,
        salinity_psu=32.5,
        dissolved_oxygen_mg_l=5.4,
        sidescan_substrate="ECOTONO_ARENA_CONCHAL",
    )
    res_opt = controller.analyze_subsea_frame_and_adapt_route(25.61, -109.02, optimal_frame)
    assert res_opt["classification"] == "CORREDOR_JAIBA_CONFIRMADO_IN_SITU"
    assert res_opt["action"] == "DEPLOY_TRAP_LINE_AND_SWEEP"
    assert res_opt["sonar_freq_khz"] == 1200
    assert len(res_opt["zigzag_waypoints"]) == 6

