# 06. Operaciones Marítimas, Protocolos LARS y Contingencias

## Metadata de Control
* **Módulo:** Operaciones en Altamar y Seguridad Marítima.
* **Propósito:** Procedimientos de cubierta en el Barco Nodriza, sistema de botadura y recuperación (LARS), modos de falla y seguridad de la flota en el Golfo de California.

---

## 1. Rol Operativo del Barco Nodriza y Dinámica de Flota
* **Misión del Barco Nodriza:**
  * Remolque y abastecimiento logístico de 20 a 50 pangas durante mareas de pesca de varios días.
  * Planta de frío / hielo preliminar para conservar el camarón fresco capturado por las pangas.
  * Centro de operaciones técnicas: Estación de carga de baterías para el USV, mástil de radioenlace y estación del capitán.
* **Coordinación con Pangas:**
  * Las pangas reciben el vector de pesca derivado del USV directamente desde el Barco Nodriza vía radio VHF marina convencional (Canal 16/Canales de trabajo de la cooperativa).

---

## 2. Sistema LARS (Launch and Recovery System - Botadura y Recuperación)

### Procedimiento de Botadura (23:30 hrs)
1. **Inspección Pre-vuelo:** Verificación de voltaje de celdas (>25.2V), fijación de sensores, sellos de escotillas y prueba de link LoRa.
2. **Maniobra de Puesta en Agua:**
   * Utilización de pescante/pluma de carga o rampa de popa en el Barco Nodriza.
   * Liberación rápida mediante gancho hidrostático o cabo de desenganche manual.
3. **Inicio de Misión:** El USV realiza un patrón de calibración en círculo a 50 m del barco y se enruta de forma autónoma al primer waypoint.

### Procedimiento de Recuperación (06:00 - 07:00 hrs)
1. **Aproximación:** El USV navega a un punto de espera (*Holding Pattern*) a 100 m del Barco Nodriza.
2. **Captura:** Asistencia con guía de cabo flotante y enganche a cuna de izaje.
3. **Mantenimiento en Cubierta:** Enjuague inmediato con agua dulce (desalinización de thrusters y conectores), descarga de telemetría completa por Wi-Fi de alta velocidad y conexión al cargador rápido.

---

## 3. Matriz de Failsafes y Contingencias Autónomas

| Condición de Falla | Acción Autónoma del USV | Notificación a Cubierta |
| :--- | :--- | :--- |
| **Pérdida de Enlace LoRa (> 10 min)** | Activa modo *Return-To-Launch* (RTL) navegando hacia la última posición conocida del Barco Nodriza. | Envío de paquete de socorro vía satelital Iridium con posición actual. |
| **Batería Crítica (< 15% SoC)** | Apaga sensores de carga útil, reduce velocidad a 1.5 nudos y regresa directo a coordenadas del barco. | Alarma sonora y visual en el dashboard del Barco Nodriza. |
| **Enredo en Hélice / Redes / Algas** | Inversión pulsada de motores (anti-tangle routine) 3 ciclos; si persiste, apaga propulsión para evitar quemar ESC. | Enciende baliza estroboscópica marina de alta visibilidad y transmite alerta de varamiento. |
| **Deriva Fuera de Geocerca Costera** | Detención de motores, anclaje virtual (loiter / dynamic positioning). | Reporte de salida de zona de seguridad. |

---

## 4. Límites Operativos Ambientales (Golfo de California)
* **Estado del Mar (Sea State):** Máximo Escala Beaufort 3 a 4 (olas de 0.5 a 1.2 metros). Por encima de esto, la prospección acústica se degrada por burbujas de aire superficiales.
* **Corrientes de Marea:** Capacidad del USV para vencer corrientes de hasta 2.5 nudos en boca de esteros (Topolobampo / Agiabampo).
* **Protección Mecánica:** Rejillas de tobera protectoras en los propulsores para evitar ingreso de cabos, redes de deriva y fauna marina.
