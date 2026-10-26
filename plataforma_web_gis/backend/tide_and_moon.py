"""
ETAPA 1 — Motor Astronómico y de Dinámica de Mareas (Golfo de California)
Calcula:
- Fase Lunar exacta e iluminación (%) (ciclo sinódico de 29.530588 días)
- Coeficiente de Marea Viva / Muerta (crítico para emergencia nocturna del camarón)
- Velocidad estimada de corriente de vaciante (reflujo en nudos) en las bocas de
  Topolobampo/Ohuira y Bahía de Kino/Estero La Cruz.
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any


SYNODIC_MONTH_DAYS = 29.530588853
KNOWN_NEW_MOON_UTC = datetime(2026, 1, 18, 19, 52, tzinfo=timezone.utc)


def calculate_lunar_and_tidal_state(target_dt: datetime = None, zona: str = "Topolobampo-Ohuira") -> Dict[str, Any]:
    """
    Devuelve el estado lunar y mareográfico para alimentar el algoritmo HSI nocturno y diurno.
    """
    if target_dt is None:
        target_dt = datetime.now(timezone.utc)
    elif target_dt.tzinfo is None:
        target_dt = target_dt.replace(tzinfo=timezone.utc)

    days_since_new = (target_dt - KNOWN_NEW_MOON_UTC).total_seconds() / 86400.0
    lunar_age_days = days_since_new % SYNODIC_MONTH_DAYS
    phase_ratio = lunar_age_days / SYNODIC_MONTH_DAYS  # 0.0 = Luna Nueva, 0.5 = Luna Llena

    # Iluminación del disco lunar (0 a 100%)
    illumination_pct = round((1.0 - math.cos(2.0 * math.pi * phase_ratio)) * 50.0, 1)

    # Nombre de la fase lunar
    if phase_ratio < 0.06 or phase_ratio > 0.94:
        phase_name = "Luna Nueva (Marea Viva Óptima Camarón)"
    elif 0.44 <= phase_ratio <= 0.56:
        phase_name = "Luna Llena (Marea Viva de Reflujo Fuerte)"
    elif 0.19 <= phase_ratio <= 0.31:
        phase_name = "Cuarto Creciente (Marea Muerta)"
    elif 0.69 <= phase_ratio <= 0.81:
        phase_name = "Cuarto Menguante (Marea Muerta)"
    elif phase_ratio < 0.5:
        phase_name = "Creciente Iluminante"
    else:
        phase_name = "Menguante"

    # Coeficiente de marea viva (máximo en Luna Nueva y Luna Llena: cos(4*pi*phase_ratio))
    spring_neap_index = (math.cos(4.0 * math.pi * phase_ratio) + 1.0) / 2.0  # 0.0 a 1.0

    # Velocidad máxima de vaciante en bocas según zona y marea viva
    base_knots = 2.4 if zona == "Topolobampo-Ohuira" else 2.1
    ebb_speed_knots = round(base_knots + 1.6 * spring_neap_index, 2)

    # Score de actividad biológica de camarón (mayor migración en reflujo de marea viva)
    shrimp_tide_score = round(70.0 + 28.0 * spring_neap_index, 1)

    return {
        "timestamp_utc": target_dt.strftime("%Y-%m-%d %H:%M UTC"),
        "zona": zona,
        "edad_lunar_dias": round(lunar_age_days, 1),
        "iluminacion_lunar_pct": illumination_pct,
        "fase_lunar": phase_name,
        "indice_marea_viva": round(spring_neap_index * 100.0, 1),
        "velocidad_reflujo_nudos": ebb_speed_knots,
        "score_actividad_marea": shrimp_tide_score,
        "recomendacion_marea": (
            f"Reflujo estimado de {ebb_speed_knots} nudos en garganta de boca. "
            "El USV Trimarán 48V opera con sus 2x 3.0 kW sobrado de empuje para sostener 3.0 nudos de barrido."
        ),
    }
