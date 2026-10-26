# 02. Bitácora de Investigación y Registro de Decisiones Técnicas

## Metadata de Control
* **Proyecto:** Analítica Predictiva y Validación USV para Pesca de Camarón (Topolobampo - Bahía de Kino).
* **Propósito:** Registro acumulativo de experimentos, selección de componentes, pruebas de campo y decisiones de arquitectura (ADR).
* **Guía de Llenado para NotebookLM:** Usar enunciados directos y datos concretos (cifras, modelos, frecuencias, protocolos). Evitar narrativa conversacional para conservar tokens y optimizar la recuperación semántica.

---

## 1. Matriz de Estado de Subsistemas

| ID | Subsistema | Estado Actual | Foco de Investigación Inmediato |
| :--- | :--- | :--- | :--- |
| **SUB-01** | Telemetría Satelital | En diseño | Fuentes abiertas vs. comerciales (latencia y resolución SST/Clorofila). |
| **SUB-02** | Plataforma USV / Catamarán | En diseño | Hidrodinámica, autonomía eléctrica, calado en bahías someras. |
| **SUB-03** | Carga Útil (Sensores) | En evaluación | Selección de ecosonda/sonar biomásico vs. interferencia acústica. |
| **SUB-04** | Enlace de Comunicaciones | En evaluación | Redundancia RF de largo alcance (LoRa/mesh) + backup satelital. |
| **SUB-05** | Modelo de Fusión y Entrega | En definición | Pipeline de correlación y generación del vector antes de las 06:00 AM. |

---

## 2. Registro de Decisiones de Arquitectura (ADR)

### ADR-001: Desacoplamiento de Sensores Acústicos del Barco Nodriza
* **Fecha:** 2026-10-18
* **Decisión:** Descartar instrumentación en casco de embarcación mayor; delegar 100% de prospección in situ a USV.
* **Justificación:** Motores diésel generan cavitación destructiva para lecturas acústicas; calado del barco nodriza impide navegación en bajos costeros.
* **Impacto:** Menor costo de instrumentación pesada; requerimiento estricto de autonomía y enlace de datos en el USV.

### ADR-002: Tren Motriz Híbrido Serie (Generador Inverter + Buffer LiFePO4)
* **Fecha:** 2026-10-18
* **Decisión:** Adoptar esquema híbrido serie (generador inverter de 2 kW + baterías LiFePO4 24V/48V) en lugar de banco puramente eléctrico.
* **Justificación:** Misión nocturna de 7 horas continuas contra corrientes de 2.5 nudos exigiría >150 kg de baterías. El generador permite tránsito y recarga, apagándose por software al entrar al polígono para escaneo 100% silencioso.
* **Impacto:** Autonomía virtual ilimitada con 15–20 L de gasolina; cero ruido acústico en adquisición de sonar.

### ADR-003: Pipeline Satelital Costero Propio en Python vs. Software Comercial
* **Fecha:** 2026-10-18
* **Decisión:** Descartar plataformas comerciales (Zunibal, Marine Instruments, CatSat) y construir pipeline automatizado con Google Earth Engine (Sentinel-2) y Copernicus Marine (CMEMS).
* **Justificación:** El software comercial usa píxeles de 1–4 km que quedan ciegos o en blanco en los primeros 2–5 km de costa (2 a 15 brazas). Sentinel-2 ofrece resolución de 10–20 m para detectar plumas estuarinas ("chocolatito") a costo \$0 USD.
* **Impacto:** Ventaja competitiva crítica en aguas someras frente a bocas de esteros; ahorro total de licencias anuales de \$10k–\$25k USD.

### ADR-004: Compartimentación Estanca con Mamparas vs. Espuma de Poliuretano
* **Fecha:** 2026-10-18
* **Decisión:** Flotadores cilíndricos (HDPE Tubomex PAD RD 21/26 o aluminio) divididos por mamparas herméticas independientes; descartar relleno masivo de espuma.
* **Justificación:** La espuma absorbe agua salada por delaminación con el tiempo, añadiendo hasta 40% de peso muerto imposible de drenar. Las mamparas estancas garantizan flotabilidad positiva incluso con rotura parcial.
* **Impacto:** Mayor vida útil, peso en seco constante y registros de inspección con válvulas de purga.

### ADR-005: Modelo Económico de Presupuesto en "3 Bolsas"
* **Fecha:** 2026-10-18
* **Decisión:** Presentar cotización ejecutiva dividida en: Bolsa 1 (Compras EE.UU. con tarjeta del cliente a costo real), Bolsa 2 (Maquila y compras México) y Bolsa 3 (Honorarios de ingeniería cibernética).
* **Justificación:** Brinda 100% de transparencia financiera a los socios armadores, elimina la sospecha de márgenes inflados en equipos caros (sensores/Starlink) y protege los honorarios técnicos.

### ADR-006: Arquitectura Trimarán con Pontón Central y Disipador de Olas (Wave Deflector)
* **Fecha:** 2026-10-18
* **Decisión:** Modificar el pontón de aluminio añadiendo un pontón/sección central y un deflector de olas a $45^\circ$ en proa.
* **Justificación:** El pontón central aloja el generador, combustible y baterías en el punto más bajo (línea de crujía), reduciendo el centro de gravedad. Los dos flotadores laterales proporcionan estabilidad transversal anti-rolido para que el haz del sonar no se distorsione. El deflector rompe el oleaje corto y protege los paneles solares.
* **Impacto:** Plataforma hidrodinámicamente estable para Beaufort 3-4 con espacio de servicio cómodo.

### ADR-007: Geoposicionamiento y Rumbo Satelital Dual u-blox ZED-F9P (Moving Baseline)
* **Fecha:** 2026-10-18
* **Decisión:** Reutilizar dos módulos GNSS u-blox ZED-F9P existentes en configuración Moving Baseline RTK; prescindir de brújula magnética para navegación.
* **Justificación:** Los campos electromagnéticos de los motores (40A–80A DC) y el generador corrompen las brújulas magnéticas. El Dual F9P proporciona *True Yaw* satelital con precisión de $0.1^\circ$ inmune a interferencias, ahorrando \$950 USD al cliente.
* **Impacto:** Navegación autónoma de precisión sin calibración de brújula en altamar.

---

## 3. Entradas de Investigación y Pruebas (Registro Cronológico)

### Plantilla de Entrada Estándar (Copiar y pegar para nuevas entradas)
```markdown
### [ENT-XXX] YYYY-MM-DD | Subsistema: [SUB-0X] | Tema: [Título conciso]
* **Objetivo:** [Qué se busca probar o resolver]
* **Parámetros / Componentes Evaluados:** [Modelos, frecuencias, resoluciones, librerías, costos]
* **Resultados / Hallazgos:** [Datos medidos, limitaciones detectadas, métricas clave]
* **Decisión Técnica:** [Aceptado, Rechazado, Requiere prueba adicional]
* **Pendientes / Bloqueos:** [Siguiente paso crítico]
```

---

### [ENT-001] 2026-10-18 | Subsistema: SUB-01 | Fuentes de Datos Oceanográficos Satelitales
* **Objetivo:** Seleccionar fuentes satelitales con actualización diaria para corte nocturno (10:00 PM).
* **Parámetros / Componentes Evaluados:**
  * Copernicus Marine Service (CMEMS): SST y Chl-a (resolución ~1 km - 4 km).
  * NASA MODIS / VIIRS (SST nocturna, reflectancia espectral).
  * NOAA Coral Reef Watch / CoastWatch (anomalías térmicas superficiales).
* **Resultados / Hallazgos:**
  * Cobertura de nubes en Golfo de California suele ser baja fuera de época de ciclones, favoreciendo sensores ópticos/infrarrojos.
  * Se requiere pipeline automatizado que descargue el producto antes de las 22:00 hrs para dar ventana de procesamiento y salida al USV.
* **Decisión Técnica:** Definir pipeline en Python para ingesta automática CMEMS/NOAA como baseline sin costo de licencias.
* **Pendientes / Bloqueos:** Evaluar latencia exacta de disponibilidad del pase nocturno en la zona Topolobampo - Bahía de Kino.

---

### [ENT-002] 2026-10-18 | Subsistema: SUB-03 | Sensórica para Detección de Camarón en USV
* **Objetivo:** Determinar la firma acústica o método de detección directo/indirecto para camarón café/azul.
* **Parámetros / Componentes Evaluados:**
  * Ecosondas bi-frecuencia (e.g., 200 kHz / 455 kHz / CHIRP de alta resolución).
  * Sonar de barrido lateral (Side Scan Sonar) de bajo consumo.
  * Sensores complementarios: Turbidez (nefelometría), salinidad/CTD y temperatura de fondo.
* **Resultados / Hallazgos:**
  * El camarón bentónico tiene target strength (TS) muy bajo y suele estar enterrado o pegado al fondo; la detección indirecta (ecotono del fondo, mezcla de turbidez/temperatura y agregación biológica) es indispensable.
* **Decisión Técnica:** Mantener prospección híbrida: acústica multifrecuencia en el USV + correlación con parámetros fisicoquímicos locales.
* **Pendientes / Bloqueos:** Cotizar e investigar módulos de sonar OEM de bajo consumo (e.g., Airmar, Lowrance OEM, Blue Robotics Ping360).

---

## 4. Banco de Parámetros Clave y Constantes del Entorno
* **Especies Objetivo:** Camarón Azul (*Litopenaeus stylirostris*), Camarón Café (*Farfantepenaeus californiensis*).
* **Rango Batimétrico Habitual de Pesca:** 5 a 30 brazas (aprox. 9 a 55 metros), variando en esteros y mar abierto.
* **Ventana Temporal Crítica:**
  * Ingesta y Poligonización: 22:00 - 23:30 hrs.
  * Muestreo USV: 00:00 - 05:00 hrs.
  * Despacho de Coordenadas al Barco Nodriza: < 06:00 hrs.
* **Enlace de Contingencia:** Coordenadas en formato compacto (SMS satelital / paquete comprimido NMEA) si la red de banda ancha falla.
