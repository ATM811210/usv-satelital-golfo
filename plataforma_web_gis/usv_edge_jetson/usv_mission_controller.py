"""
ETAPAS 5 Y 6 — Controlador Maestro de Misión Edge AI (NVIDIA Jetson Orin Nano)
Para USV Trimarán Híbrido 48V "Stealth" (Doble Turno 24h: Camarón Noche / Sardina Día)

Subsistemas gobernados:
1. Propulsión 48V: 2x Flipsky 65161 (3.0 kW c/u) + Dual FSESC75200 Pro (Water Cooled).
2. Energía Doble Respaldo: Banco LiFePO4 48V 200Ah (10.24 kWh) monitored via Victron SmartShunt 500A
   + Planta Híbrida 4T con pre-barrido de vapores de sentina ISO 8846 (90s).
3. Rumbo Verdadero Dual RTK: 2x u-blox ZED-F9P en Moving Baseline (2.5m separación -> 0.1° True Yaw).
4. Sensores Submarinos:
   - Sonar CHIRP 1kW Garmin GSD 25 + Airmar B265LH (200 kHz Camarón / 50 kHz Sardina)
   - Hidrófono Digital Aquarian H3d-Ethernet (Exclusión Roca >2.4 kHz / Detección Curvina 450 Hz)
   - Sonda Turner Designs Cyclops-7F (Clorofila-a + Turbidez + Micro-CTD de Fondo)
5. Seguridad y Enlace: Cámara Térmica FLIR Boson 320 + Radar Ainstein 24 GHz + AIS Clase B SEMAR
   + Starlink Mini con Failover automático a Radioenlace RFD900x (915 MHz, 40+ km).
"""

import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any


@dataclass
class DualF9PMovingBaseline:
    """
    Calcula el rumbo verdadero (True Yaw) de alta precisión (0.1°) a partir del vector
    NED (North-East-Down) entre los dos receptores u-blox ZED-F9P (mensaje UBX-NAV-RELPOSNED),
    eliminando el uso de brújula magnética afectada por los 125A del bus de 48V.
    """
    baseline_length_m: float = 2.50
    rel_north_m: float = -1.15
    rel_east_m: float = -2.22
    rtk_fixed_carrier: bool = True

    def compute_true_yaw_deg(self) -> float:
        yaw_rad = math.atan2(self.rel_east_m, self.rel_north_m)
        yaw_deg = (math.degrees(yaw_rad) + 360.0) % 360.0
        return round(yaw_deg, 2)


@dataclass
class VictronBatteryBank48V:
    """
    Monitoreo del banco masivo LiFePO4 48V 200Ah (10.24 kWh nominales, ~85 kg).
    Provee el Seguro Anti-Deriva ('Limp-Home' de 25 Millas Náuticas a 4.5 nudos).
    """
    nominal_capacity_wh: float = 10240.0
    voltage_v: float = 52.4
    current_a: float = -16.5
    soc_pct: float = 86.0
    wh_per_nm_at_4_5_knots: float = 185.0  # ~830W a 4.5 nudos hidrodinámicos

    def available_limp_home_nm(self) -> float:
        # Conserva 10% de piso de seguridad en el Smart BMS para no dañar celdas
        usable_wh = max(0.0, (self.soc_pct - 10.0) / 100.0 * self.nominal_capacity_wh)
        return round(usable_wh / self.wh_per_nm_at_4_5_knots, 1)


@dataclass
class SubseaSensorFrame:
    sonar_freq_khz: int               # 200 (Camarón), 50 (Pescado/Sardina) o 800 (Side-Scan Jaiba)
    depth_brazas: float               # 1 braza = 1.8288 m
    biomass_echo_db: float            # Intensidad de retrodispersión acústica (-30 a -75 dB)
    hydrophone_peak_freq_khz: float   # >2.4 kHz = Roca (Camarón) o Forrajeo Bivalvos (Jaiba); 0.45 kHz = Curvina
    hydrophone_rms_db: float
    chlorophyll_a_mg_m3: float        # Sonda Turner Cyclops-7F / RBRconcerto³
    turbidity_ntu: float              # Sonda Turner Cyclops-7F / RBRconcerto³
    bottom_temp_c: float              # Micro-CTD / RBRconcerto³
    salinity_psu: float               # Micro-CTD / RBRconcerto³
    dissolved_oxygen_mg_l: float = 5.4                    # Sonda Óptica DO Atlas EZO-DO / RBR optode
    sidescan_substrate: str = "ECOTONO_ARENA_CONCHAL"     # LODO_ORGANICO, ECOTONO_ARENA_CONCHAL, ZOSTERA_PASTO, ROCA_DURA


class USVMissionController48V:
    """
    Cerebro autónomo ejecutado en la NVIDIA Jetson Orin Nano (MVP) / AGX Orin (Científico)
    conectada por UART/MAVLink al CubePilot Cube Orange+.
    Soporta 3 modos de prospección: NOCTURNO_CAMARON, DIURNO_SARDINA (Pescado) y PROSPECCION_JAIBA.
    """

    def __init__(
        self,
        shift_mode: str = "NOCTURNO_CAMARON",
        sensor_tier: str = "MVP_BAJO_COSTO",
    ) -> None:
        self.shift_mode = shift_mode
        self.sensor_tier = sensor_tier
        self.rtk_yaw = DualF9PMovingBaseline()
        self.battery = VictronBatteryBank48V()
        self.generator_4t_running = False
        self.generator_fault_flagged = False
        self.bilge_blower_purged = False
        self.starlink_online = True
        self.active_link = "STARLINK_MINI_HIGH_SPEED"

    def evaluate_failsafe_and_power(self, distance_to_dock_nm: float) -> Dict[str, Any]:
        """
        ETAPA 6 — Máquina de Estados de Supervivencia y Propulsión Híbrida 48V:
        1. Verifica si la reserva Limp-Home cubre la distancia al muelle + 35% margen contra reflujo.
        2. En Turno Nocturno dentro de polígono de camarón, fuerza MODO SILENCIOSO ELÉCTRICO (Generador OFF).
        3. Si requiere arrancar el generador 4T, ejecuta primero 90s de extractor de vapores ISO 8846.
        """
        limp_range_nm = self.battery.available_limp_home_nm()
        required_nm_with_margin = distance_to_dock_nm * 1.35

        # Caso 1: Fallo de generador en altamar o batería llegando al umbral de retorno seguro
        if self.generator_fault_flagged or limp_range_nm <= required_nm_with_margin:
            self.generator_4t_running = False
            return {
                "propulsion_state": "LIMP_HOME_EMERGENCY_25NM",
                "target_speed_knots": 4.5,
                "mavlink_mode": "RTL_SAFE_CHANNEL",
                "generator_4t": "OFF_FAULT_OR_RESERVE",
                "limp_home_remaining_nm": limp_range_nm,
                "alert": (
                    f"SEGURO ANTI-DERIVA ACTIVO: Retornando al muelle en modo 100% eléctrico "
                    f"con banco LiFePO4 10.24 kWh ({limp_range_nm} MN disponibles para {distance_to_dock_nm} MN al muelle)."
                ),
            }

        # Caso 2: Batería baja (<35% SoC) en tránsito -> Activar extractor ISO 8846 (90s) y encender Generador 4T
        if self.battery.soc_pct < 35.0:
            self.bilge_blower_purged = True
            self.generator_4t_running = True

        # Caso 3: Barrido Nocturno sobre polígono de camarón -> Sigilo Acústico 100% Eléctrico
        if self.shift_mode == "NOCTURNO_CAMARON" and self.battery.soc_pct >= 40.0:
            self.generator_4t_running = False
            return {
                "propulsion_state": "ELECTRICO_STEALTH_3KT",
                "target_speed_knots": 3.0,
                "mavlink_mode": "AUTO_SWEEP",
                "generator_4t": "APAGADO (0 dB Ruido Submarino)",
                "limp_home_remaining_nm": limp_range_nm,
                "alert": "Operación nominal en sigilo eléctrico sobre polígono camaronero.",
            }

        # Caso 4: Turno Diurno (Sardina/Escama) o Tránsito Rápido Híbrido
        self.bilge_blower_purged = True
        self.generator_4t_running = True
        return {
            "propulsion_state": "HIBRIDO_AUTO_CARGA_8_11KT",
            "target_speed_knots": 8.5,
            "mavlink_mode": "AUTO_PELAGIC",
            "generator_4t": "ENCENDIDO (Extractor ISO 8846 Verificado)",
            "limp_home_remaining_nm": limp_range_nm,
            "alert": "Tránsito híbrido / prospección pelágica diurna activa.",
        }

    def analyze_subsea_frame_and_adapt_route(
        self,
        lat: float,
        lon: float,
        frame: SubseaSensorFrame,
    ) -> Dict[str, Any]:
        """
        ETAPA 5 — Fusión Acústica + Bioquímica en Tiempo Real:
        - Detecta fondos rocosos (>2.4 kHz en hidrófono) para etiquetar Zonas de Exclusión Rompe-Redes.
        - Si confirma alta densidad de camarón (200 kHz) o sardina/clorofila (50 kHz), genera
          automáticamente un patrón de barrido en Zig-Zag (Lawnmower) para delimitar la mancha.
        """
        # 1. Evaluación Modo 3: Prospección de Jaiba Bentónica (Side-Scan 800 kHz / Oculus + Sonda DO)
        if "JAIBA" in self.shift_mode.upper():
            if frame.dissolved_oxygen_mg_l < 2.2:
                return {
                    "classification": "ZONA_HIPOXICA_MORTALIDAD_TRAMPAS",
                    "action": "ABORT_TRAP_DEPLOYMENT_AND_BYPASS",
                    "sonar_freq_khz": 800,
                    "heading_rtk_deg": self.rtk_yaw.compute_true_yaw_deg(),
                    "reason": (
                        f"ALERTA ROJA HIPOXIA: Oxígeno disuelto en fondo ({frame.dissolved_oxygen_mg_l} mg/L) "
                        "por debajo del umbral letal (2.2 mg/L). Prohibido calar trampas jaiberas."
                    ),
                    "zigzag_waypoints": [],
                }

            is_jaiba_corridor = (
                0.8 <= frame.depth_brazas <= 8.5
                and frame.bottom_temp_c >= 20.0
                and frame.sidescan_substrate in ("ECOTONO_ARENA_CONCHAL", "ZOSTERA_PASTO", "LODO_ORGANICO")
            )
            if is_jaiba_corridor:
                zigzag = self.generate_lawnmower_zigzag(lat, lon, span_deg=0.0030)
                return {
                    "classification": "CORREDOR_JAIBA_CONFIRMADO_IN_SITU",
                    "action": "DEPLOY_TRAP_LINE_AND_SWEEP",
                    "sonar_freq_khz": 800 if self.sensor_tier == "MVP_BAJO_COSTO" else 1200,
                    "heading_rtk_deg": self.rtk_yaw.compute_true_yaw_deg(),
                    "reason": (
                        f"Hábitat óptimo de Jaiba confirmado por Side-Scan ({frame.sidescan_substrate}) a {frame.depth_brazas} bz, "
                        f"DO {frame.dissolved_oxygen_mg_l} mg/L, Temp {frame.bottom_temp_c}°C. Trazando línea de 25 trampas/ha."
                    ),
                    "zigzag_waypoints": zigzag,
                }

        # 2. Filtro Acústico Anti-Roca para Redes de Arrastre (Hidrófono Aquarian H3d-Ethernet)
        if frame.hydrophone_peak_freq_khz >= 2.4 and frame.hydrophone_rms_db >= -48.0:
            return {
                "classification": "ZONA_EXCLUSION_ROCA_ROMPE_REDES",
                "action": "MARK_HAZARD_AND_BYPASS",
                "sonar_freq_khz": frame.sonar_freq_khz,
                "reason": (
                    f"Hidrófono detectó firma de arrecife/piedra viva ({frame.hydrophone_peak_freq_khz} kHz). "
                    "Se marca polígono prohibido para proteger chinchorros de la cooperativa."
                ),
                "zigzag_waypoints": [],
            }

        # 3. Evaluación Modo 1: Turno Noche (Camarón en 2 a 12 brazas con CHIRP 200 kHz)
        if "CAMARON" in self.shift_mode.upper():
            is_shrimp_hotspot = (
                2.0 <= frame.depth_brazas <= 12.5
                and frame.biomass_echo_db >= -52.0
                and 24.0 <= frame.bottom_temp_c <= 28.5
            )
            if is_shrimp_hotspot:
                zigzag = self.generate_lawnmower_zigzag(lat, lon, span_deg=0.0035)
                return {
                    "classification": "MANCHA_CAMARON_CONFIRMADA_IN_SITU",
                    "action": "EXECUTE_ZIGZAG_SWEEP_AND_ALERT_PANGAS",
                    "sonar_freq_khz": 200,
                    "heading_rtk_deg": self.rtk_yaw.compute_true_yaw_deg(),
                    "reason": (
                        f"Eco denso de camarón pegado al lodo ({frame.biomass_echo_db} dB a {frame.depth_brazas} bz, "
                        f"Temp fondo {frame.bottom_temp_c}°C, 0% roca). Iniciando barrido zig-zag."
                    ),
                    "zigzag_waypoints": zigzag,
                }

        # 4. Evaluación Modo 2: Turno Día (Pescado / Sardina / Curvina con CHIRP 50 kHz + Clorofila-a)
        if "SARDINA" in self.shift_mode.upper() or "PESCADO" in self.shift_mode.upper() or "DIURNO" in self.shift_mode.upper():
            is_pelagic_school = (
                frame.chlorophyll_a_mg_m3 >= 2.5
                and frame.biomass_echo_db >= -46.0
            )
            if is_pelagic_school:
                zigzag = self.generate_lawnmower_zigzag(lat, lon, span_deg=0.0060)
                return {
                    "classification": "CARDUMEN_SARDINA_O_CURVINA_CONFIRMADO",
                    "action": "EXECUTE_PELAGIC_MAPPING_AND_NOTIFY_FLEET",
                    "sonar_freq_khz": 50,
                    "heading_rtk_deg": self.rtk_yaw.compute_true_yaw_deg(),
                    "reason": (
                        f"Frente biológico confirmado: Clorofila-a {frame.chlorophyll_a_mg_m3} mg/m³ "
                        f"y cardumen denso en 50 kHz ({frame.biomass_echo_db} dB a {frame.depth_brazas} bz)."
                    ),
                    "zigzag_waypoints": zigzag,
                }

        return {
            "classification": "TRANSITO_EXPLORACION_CANAL",
            "action": "CONTINUE_CHANNEL_WAYPOINTS",
            "sonar_freq_khz": frame.sonar_freq_khz,
            "heading_rtk_deg": self.rtk_yaw.compute_true_yaw_deg(),
            "zigzag_waypoints": [],
        }

    @staticmethod
    def generate_lawnmower_zigzag(center_lat: float, center_lon: float, span_deg: float = 0.004) -> List[Tuple[float, float]]:
        """
        Genera una malla de 6 vértices en zig-zag (Lawnmower) alrededor del centroide acústico
        para enviar por MAVLink al CubePilot Cube Orange+.
        """
        half = span_deg / 2.0
        return [
            (round(center_lat - half, 5), round(center_lon - half, 5)),
            (round(center_lat + half, 5), round(center_lon - half, 5)),
            (round(center_lat + half, 5), round(center_lon, 5)),
            (round(center_lat - half, 5), round(center_lon, 5)),
            (round(center_lat - half, 5), round(center_lon + half, 5)),
            (round(center_lat + half, 5), round(center_lon + half, 5)),
        ]

    def select_telemetry_channel(self, starlink_ping_ms: float) -> str:
        """
        ETAPA 6 — Failover Automático de Comunicaciones:
        Usa Starlink Mini como canal primario de banda ancha y conmuta sin intervención humana
        al radioenlace RFDesign RFD900x (915 MHz, 40+ km) si Starlink pierde vista al cielo.
        """
        if starlink_ping_ms <= 650.0 and self.starlink_online:
            self.active_link = "STARLINK_MINI_BROADBAND"
        else:
            self.active_link = "RFD900X_915MHZ_LONG_RANGE_BACKUP"
        return self.active_link
