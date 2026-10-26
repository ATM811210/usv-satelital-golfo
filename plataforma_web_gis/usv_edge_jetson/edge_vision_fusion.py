"""
Nodo Edge AI Multicámara y Estimación Acústica de Biomasa
Ejecutado localmente en NVIDIA Jetson Orin Nano (Totalmente Desconectado).

Misión Crítica:
1. Detección perimetral nocturna mediante cámara térmica FLIR Boson 320x256 (Pangas sin luces, boyas).
2. Cálculo de Tiempo al Impacto (TTC - Time to Collision) bajo reglas COLREGs.
3. Estimación cuantitativa de biomasa de camarón (kg/ha) mediante retrodispersión acústica CHIRP 200 kHz.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class CollisionRisk(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    CRITICAL_EVASION = "CRITICAL_EVASION"


class BiomassDensityClass(str, Enum):
    NULA = "NULA"
    DISPERSA = "DISPERSA"
    COMERCIAL_MEDIA = "COMERCIAL_MEDIA"
    ALTA_CONCENTRACION_ZAFRA = "ALTA_CONCENTRACION_ZAFRA"


@dataclass
class DetectedObstacle:
    label: str                     # "panga_sin_luz", "boya_palangre", "escombro_flotante"
    confidence: float              # 0.0 a 1.0
    bearing_deg: float             # -90.0 (Babor) a +90.0 (Estribor), 0.0 = Proa
    distance_m: float              # Distancia estimada por telemetría estéreo / radar
    relative_speed_knots: float    # Velocidad de aproximación


@dataclass
class BiomassEstimate:
    density_class: BiomassDensityClass
    estimated_kg_per_hectare: float
    acoustic_confidence_pct: float
    depth_m: float
    shrimp_viable: bool            # Temperatura de fondo adecuada y libre de sustrato rocoso


class EdgeVisionFusionEngine:
    """
    Motor de fusión de sensores en borde para navegación autónoma y pesca de precisión.
    """

    def __init__(self, safe_ttc_seconds: float = 18.0) -> None:
        self.safe_ttc_seconds = safe_ttc_seconds

    def evaluate_collision_risk(
        self, obstacles: List[DetectedObstacle], own_speed_knots: float
    ) -> Tuple[CollisionRisk, Optional[DetectedObstacle]]:
        """
        Evalúa el riesgo de impacto de obstáculos detectados por FLIR Boson / RGB.
        Aplica la regla de Tiempo al Impacto (TTC = d / v_relativa).
        """
        if not obstacles:
            return CollisionRisk.NONE, None

        highest_risk = CollisionRisk.NONE
        critical_obstacle = None

        for obs in obstacles:
            if obs.confidence < 0.45:
                continue

            # Velocidad de cierre (aproximación en nudos a m/s: 1 nudo = 0.5144 m/s)
            closing_speed_knots = obs.relative_speed_knots + own_speed_knots
            if closing_speed_knots <= 0.5:
                # Obstáculo estacionario o alejándose
                closing_speed_mps = 0.5 * 0.5144
            else:
                closing_speed_mps = closing_speed_knots * 0.5144

            ttc_sec = obs.distance_m / max(closing_speed_mps, 0.1)

            # Clasificación de riesgo determinista
            if ttc_sec <= 8.0 or obs.distance_m < 25.0:
                return CollisionRisk.CRITICAL_EVASION, obs
            elif ttc_sec <= self.safe_ttc_seconds or obs.distance_m < 60.0:
                if highest_risk != CollisionRisk.CRITICAL_EVASION:
                    highest_risk = CollisionRisk.MODERATE
                    critical_obstacle = obs
            elif obs.distance_m < 120.0:
                if highest_risk == CollisionRisk.NONE:
                    highest_risk = CollisionRisk.LOW
                    critical_obstacle = obs

        return highest_risk, critical_obstacle

    @staticmethod
    def estimate_shrimp_biomass(
        echo_db: float,
        depth_brazas: float,
        hydrophone_freq_khz: float,
        bottom_temp_c: float,
    ) -> BiomassEstimate:
        """
        Modelo empírico acústico para camarón café/azul (Farfantepenaeus californiensis / Litopenaeus stylirostris):
        - Ventana batimétrica: 2 a 12 brazas (3.6m a 22m).
        - Exclusión estricta de arrecife rocoso (hidrófono > 2.4 kHz).
        - Rango térmico metabólico óptimo: 22°C a 29°C.
        - Relación Target Strength (TS): Intensidad acústica -55 dB a -35 dB.
        """
        depth_m = round(depth_brazas * 1.8288, 2)

        # 1. Filtro de exclusión por fondo rocoso
        if hydrophone_freq_khz >= 2.4:
            return BiomassEstimate(
                density_class=BiomassDensityClass.NULA,
                estimated_kg_per_hectare=0.0,
                acoustic_confidence_pct=95.0,
                depth_m=depth_m,
                shrimp_viable=False,
            )

        # 2. Filtro de profundidad biológica y temperatura
        if not (2.0 <= depth_brazas <= 12.5) or not (20.0 <= bottom_temp_c <= 31.0):
            return BiomassEstimate(
                density_class=BiomassDensityClass.NULA,
                estimated_kg_per_hectare=0.0,
                acoustic_confidence_pct=85.0,
                depth_m=depth_m,
                shrimp_viable=False,
            )

        # 3. Mapeo de retrodispersión acústica a densidad de biomasa
        # -35 dB = Saturación máxima / gran mancha
        # -55 dB = Límite inferior de detección comercial
        if echo_db >= -40.0:
            density = BiomassDensityClass.ALTA_CONCENTRACION_ZAFRA
            kg_ha = min(450.0, 200.0 + (echo_db + 40.0) * 15.0)
            conf = 92.0
        elif echo_db >= -48.0:
            density = BiomassDensityClass.COMERCIAL_MEDIA
            kg_ha = 90.0 + (echo_db + 48.0) * 12.0
            conf = 88.0
        elif echo_db >= -55.0:
            density = BiomassDensityClass.DISPERSA
            kg_ha = 25.0 + (echo_db + 55.0) * 8.0
            conf = 80.0
        else:
            density = BiomassDensityClass.NULA
            kg_ha = 0.0
            conf = 75.0

        return BiomassEstimate(
            density_class=density,
            estimated_kg_per_hectare=round(max(0.0, kg_ha), 1),
            acoustic_confidence_pct=conf,
            depth_m=depth_m,
            shrimp_viable=True,
        )
