# 04. Arquitectura de Comunicaciones y Telemetría Marina

## Metadata de Control
* **Módulo:** SUB-04 (Comunicaciones y Telemetría en Altamar).
* **Propósito:** Diseño de los enlaces de radiofrecuencia, satelital y formatos de trama para transferencia de datos en el Golfo de California sin cobertura celular.

---

## 1. Topología de Enlace en Altamar

```
┌─────────────────┐                                  ┌──────────────────────┐
│  USV Catamarán  │ ──[ LoRa 915 MHz (Telemetría) ]──►│    Barco Nodriza     │
│   (Prospección) │ ──[ RF 2.4/5.8 GHz (Datos/Dump) ]─►│   (Centro de Mando)  │
└─────────────────┘                                  └──────────┬───────────┘
         │                                                      │
         │ [Backup SBD Iridium]                                 │ [Starlink Marítimo /
         ▼                                                      ▼  Red 4G Costera]
   Satélite Iridium ────────────────────────────────────► Nube / Base en Tierra
```

---

## 2. Niveles de Comunicación y Hardware de Radio

### Nivel 1: Enlace Crítico de Control y Telemetría (Largo Alcance)
* **Tecnología:** LoRa Punto a Punto / MESH en banda ISM **915 MHz** (aprobada para México / IFT).
* **Módulos:** SX1262 / RFM95W o módems industriales tipo RFDesign (RFD900x con amplificación de hasta 1W).
* **Alcance Esperado:** 5 a 15 km en línea de vista marítima (antena omnidireccional en USV + antena colineal/directiva elevada en mástil del Barco Nodriza).
* **Tasa de Transmisión:** 1.2 kbps – 19.2 kbps (optimizada para latencia y robustez ante ruido RF).

### Nivel 2: Enlace Local de Alto Ancho de Banda (Proximidad / LARS)
* **Tecnología:** Wi-Fi 5.8 GHz (Ubiquiti Bullet / Mikrotik marítimo).
* **Propósito:** Descarga rápida de ecogramas completos, logs brutos y actualización de waypoints cuando el USV se encuentra a menos de 500 m del Barco Nodriza.

### Nivel 3: Enlace de Respaldo Satelital (Falla Total de RF)
* **Módulo:** Transceptor Iridium SBD (Short Burst Data) tipo RockBLOCK 9603.
* **Propósito:** Envío exclusivo de latidos (*heartbeats*) con coordenadas GPS, voltaje de batería y estado de alarma en caso de pérdida de enlace de radio. Payload: 50 bytes por mensaje.

---

## 3. Protocolos de Trama y Empaquetado de Datos

Para minimizar el consumo de ancho de banda y asegurar que los mensajes lleguen íntegros vía LoRa:

### A. Trama Binaria Compacta de Telemetría (USV $\to$ Barco Nodriza)
* **Estructura (32 Bytes totales):**
  * `Header` (2 bytes): `0xCA 0xFE`
  * `Timestamp UTC` (4 bytes): `uint32`
  * `Latitud` (4 bytes): `int32` (escala $1\times 10^7$)
  * `Longitud` (4 bytes): `int32` (escala $1\times 10^7$)
  * `Rumbo / Velocidad` (2 bytes): `uint8` rumbo relativo + `uint8` nudos $\times 10$
  * `Batería / Estado` (2 bytes): `uint8` % SoC + `uint8` flags de error
  * `Índice de Biomasa Acústica` (4 bytes): `float32` (nivel de reflectancia de fondo integrada)
  * `Turbidez / Temperatura` (4 bytes): `uint16` NTU $\times 10$ + `int16` $^\circ\text{C}\times 100$
  * `CRC16` (2 bytes): Verificación de redundancia cíclica

### B. Formato de Despacho al Capitán (< 06:00 AM)
* **Objetivo:** Compatibilidad directa con plotters marinos de cabina (Garmin, Furuno, Simrad) y tablets resistentes.
* **Formatos Soportados:**
  * **Sentencias NMEA 0183 (`$GPGGA`, `$GPWPT`, `$GPRTE`):** Inyección directa al sistema de navegación del barco nodriza.
  * **Archivo GPX / GeoJSON:** Carga rápida en apps de navegación tipo Navionics, TimeZero u OpenCPN.
  * **Mensaje Resumen de Texto (SMS satelital / WhatsApp en puerto):**
    > *"REPORTE PROSPECCIÓN 05:30 AM: Polígono Primario [25.782°N, -109.412°W]. Profundidad óptima: 14 brazas. Índice biomasa: ALTO (87%). Fondo: Fango blando."*
