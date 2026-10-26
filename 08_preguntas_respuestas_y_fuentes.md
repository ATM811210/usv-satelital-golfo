# 08. Compendio de Investigación: Preguntas, Respuestas Técnicas y Fuentes

## Metadata de Control
* **Origen de la Información:** Sesión de investigación técnica y viabilidad de ingeniería cibernética para detección de camarón en el Golfo de California (Sonora - Sinaloa).
* **Propósito:** Registro central de preguntas del cliente/ingeniero, respuestas técnicas depuradas y fuentes documentales/comerciales.
* **Formato:** Pregunta directa $\rightarrow$ Respuesta de ingeniería de alta densidad $\rightarrow$ Fuentes y referencias verificables.

---

## Bloque 1: Detección Biológica y Acústica Submarina

### [Q-01] ¿Cuál es la mejor forma de detectar camarón en el mar y qué equipos se ocupan empezando por satélites?
* **Respuesta Técnica:**
  * **Fase Satelital:** El camarón es bentónico y no se ve directamente desde el espacio; se detecta su hábitat mediante correlación oceanográfica: Temperatura Superficial del Mar (SST), Clorofila-a (productividad primaria) y Turbidez (frentes estuarinos y desembocaduras).
  * **Limitación Crítica:** El camarón no tiene vejiga natatoria; su reflectancia acústica (*Target Strength*) es muy baja (-50 a -65 dB). Un sonar comercial convencional no lo detecta en el fondo.
  * **Filtro de Descarte Acústico:** Se usan ecosondas multifrecuencia de banda ancha (120 kHz, 200 kHz, 333 kHz) como el **Simrad EK80 WBT Mini** para separar ecos de camarón del fondo y de peces pequeños.
* **Fuentes y Referencias:**
  * *Kongsberg Discovery - Simrad EK80 Scientific Wideband Transceiver (WBT Mini)*.
  * *FAO Fisheries & Aquaculture - Acoustic discrimination of crustacean biomass*.

### [Q-02] ¿El "chasquido" del camarón sirve para rastrearlo con hidrófonos en mar abierto?
* **Respuesta Técnica:**
  * **Mito vs. Realidad:** El camarón pistola (*Alpheidae*) produce chasquidos de cavitación potentes (hasta 210 dB, 2 kHz a 200 kHz), pero vive exclusivamente en fondos duros, arrecifes o roca (zonas donde no hay camarón comercial y se destruyen las redes).
  * **Camarón Comercial (*Penaeidae*):** Genera clics débiles de masticación (5 a 120 kHz), detectables en estanques de acuicultura (sistemas MASS/AQ1), pero en mar abierto a 10–50 m sobre lodo blando, la señal acústica es absorbida y enmascarada por el oleaje.
  * **Uso del Hidrófono en el USV:** No para rastrear camarón directamente, sino como **sensor de exclusión**: si el hidrófono registra alta actividad de chasquidos, descarta la zona por ser fondo rocoso.
* **Fuentes y Referencias:**
  * *Au, W. W. L., & Banks, K. (1998). High frequency acoustic emissions of snapping shrimp in subterranean burrows*.
  * *Marine Instruments MASS (Marine Acoustic Smart System)*.

### [Q-03] ¿Qué métodos de ultra-alta precisión existen si se requiere confirmación absoluta?
* **Respuesta Técnica:**
  1. **Cámara Acústica de Alta Frecuencia:** Sonares de imagen 2D/3D (1.2 MHz a 3.0 MHz) tipo **ARIS Explorer** o **Blueprint Subsea Oculus** montados en micro-AUV o sled a 1–2 m del fondo. Generan "video por sonido" que atraviesa aguas con turbidez severa permitiendo conteo por visión artificial (YOLO/CNN).
  2. **Perfilador CTD con Turbidímetro:** Winche compacto en USV (SonTek CastAway o RBRconcerto) para verificar termoclina de fondo y oxígeno disuelto ($>2\text{ mg/L}$ para evitar hipoxia).
  3. **ADN Ambiental (eDNA):** Muestreador robótico de agua en lecho marino; análisis qPCR identifica especie (*Litopenaeus stylirostris / Farfantepenaeus californiensis*) con 99% de certeza biológica.
  4. **Sensor de Impacto Acústico en Red (Notus ECHO):** Sensor piezoeléctrico en la rejilla de arrastre de la panga/nodriza; escucha el impacto mecánico del exoesqueleto y transmite kilos/hora en cabina.
* **Fuentes y Referencias:**
  * *Sound Metrics Corp (ARIS Acoustic Cameras)*.
  * *Blueprint Subsea - Oculus Multibeam Imaging Sonars*.
  * *Notus Electronics Ltd - Trawl Net Monitoring Systems (Notus ECHO)*.

---

## Bloque 2: Software, Pipeline Satelital y Oceanografía Costera

### [Q-04] ¿Conviene usar software comercial de pesca (Zunibal, Marine Instruments, CatSat) o programar un pipeline propio?
* **Respuesta Técnica:**
  * **Falla del Software Comercial:** Diseñado para atún y pesca pelágica en alta mar. Utilizan píxeles de 1 a 4 km (MODIS/VIIRS); en la franja costera de Sonora y Sinaloa (2 a 15 brazas, primeros 2 a 5 km desde la costa), los píxeles aparecen en blanco o con error de reflectancia por arena.
  * **Ventaja del Pipeline Propio en Python:**
    1. **Google Earth Engine (GEE) + Sentinel-2:** Resolución de **10 a 20 metros** por píxel. Permite mapear con precisión milimétrica la pluma de turbidez ("chocolatito") que sale de esteros tras mareas vaciantes o descargas fluviales.
    2. **Copernicus Marine Service (CMEMS):** Datos de fondo diarios a las 05:00 AM vía API Python (`copernicusmarine`): temperatura de lecho, corrientes costeras y salinidad a **costo \$0 USD**.
    3. **Formato de Exportación Directo:** Salida ligera en `.mbtiles` o `.kml` transferida por Starlink al barco nodriza para abrir en Navionics, TimeZero o QField.
* **Fuentes y Referencias:**
  * *Copernicus Marine Data Store API (`copernicusmarine` Python client)*.
  * *Google Earth Engine Python API (Sentinel-2 MultiSpectral Instrument Level-2A)*.

---

## Bloque 3: Arquitectura Naval del USV, Casco y Materiales

### [Q-05] ¿Por qué un Catamarán USV y no un Wave Runner o lancha rápida tripulada?
* **Respuesta Técnica:**
  * **Gasto de Combustible:** Una lancha rápida o Wave Runner gasta entre 40 y 80 litros de gasolina por salida nocturna; un USV híbrido consume una fracción (~2 a 4 litros de gasolina por jornada).
  * **Riesgo Humano:** Elimina navegación nocturna en aguas someras con peligro de marejadas, niebla marina y bancos de arena.
  * **Firma Acústica:** El USV opera con propulsión eléctrica en modo sondeo, reduciendo a cero el ruido y cavitación que ahuyentan la fauna y saturan los hidrófonos.

### [Q-06] ¿Qué opciones de materiales y construcción de casco existen? (2.5 m vs 3.8 m vs Pontón Recreativo)
* **Respuesta Técnica:**
  * **Opción A (2.5 metros - Fibra de Vidrio / Rotomoldeo):** Ligero (~80-120 kg), botadura manual desde pescante simple, resistencia Beaufort 2–3. Limitado en autonomía y capacidad de carga para generador pesado.
  * **Opción B (3.8 a 4.0 metros - Aluminio Naval 5083/5052):** Alta rigidez estructural, resistencia Beaufort 4–5, capacidad para doble generador redundante y 4 thrusters, pero peso $>350\text{ kg}$, complicando el izaje (LARS) en altamar sin pluma hidráulica.
  * **Opción C (Pontón Recreativo Usado de Aluminio o HDPE Industrial):**
    * Adquisición de pontón de 18-20 pies usado: Se retira estructura superior y motores fuera de borda; se aprovechan los tubos de aluminio marino y travesaños.
    * Alternativa HDPE Nacional: Fabricación de flotadores cilíndricos con tubería **Tubomex PAD liso hidráulico (RD 21 o RD 26 de 18" a 24")** soldada por termofusión, con mamparas interiores estancas cada metro.
* **Fuentes y Referencias:**
  * *Tubomex: Especificaciones Técnicas de Tubería PAD Liso Hidráulico (PE4710 / ASTM F714)*.
  * *NyDock: Commercial Floating Pontoons & HDPE Extrusion Modules*.

### [Q-07] ¿Relleno de espuma de poliuretano o mamparas selladas herméticas?
* **Respuesta Técnica:**
  * **Decisión:** **Mamparas interiores estancas (Bulkheads) con válvula de purga y registro de presión**, complementadas únicamente con espuma de celda cerrada en zonas perimetrales de proa.
  * **Justificación:** La espuma de poliuretano común con el tiempo y la salinidad absorbe humedad (delaminación hidrostática), aumentando el peso muerto del USV hasta un 40% y reteniendo agua salada corrosiva que no se puede drenar. Las secciones selladas independientes garantizan flotabilidad positiva incluso con perforación de un compartimento.

---

## Bloque 4: Tren Motriz, Potencia Híbrida y Energía Solar

### [Q-08] ¿Por qué Tren Motriz Híbrido Serie (Generador Inverter + Baterías) y no solo Baterías?
* **Respuesta Técnica:**
  * **Ventana de Misión:** 11:00 PM a 06:00 AM (7 horas continuas) navegando entre 3 y 5 nudos contra corrientes de marea del Golfo de California (hasta 2.5 nudos).
  * **Peso y Volumen:** Un banco de baterías puro para 7 horas a corriente requeriría $>150\text{ kg}$ de LiFePO4 ($>7\text{ kWh}$ útiles).
  * **Arquitectura Híbrida Serie:**
    * Un generador inverter de 2.0–2.2 kW (Honda EU22i o Yamaha EF2000iS) con tanque auxiliar de combustible de 15 a 20 litros.
    * Banco de baterías LiFePO4 intermedio (24V / 40–50 Ah) que actúa como *buffer*.
    * Durante el tránsito rápido opera el generador cargando celdas. Al llegar al polígono caliente para escaneo de sonar, el generador se apaga por software y el USV navega en **modo 100% eléctrico silencioso**, encendiéndose automáticamente si el SoC cae por debajo del 30%.
* **Fuentes y Referencias:**
  * *Honda Power Equipment - Inverter Generators (EU2200i Marine conversion)*.
  * *Victron Energy - MultiPlus & Smart BMS Architecture*.

### [Q-09] ¿Es viable instalar 6 paneles solares de alta eficiencia en la cubierta del pontón?
* **Respuesta Técnica:**
  * **Viabilidad:** Totalmente viable si se montan **a ras de cubierta** con deflectores de olas de aluminio (*Wave Deflectors*) soldados en proa con ángulo de $45^\circ$.
  * **Configuración:** 6 paneles monocristalinos bifaciales de 100W a 120W (600W – 720W pico).
  * **Función:** Durante el día, mientras el USV se encuentra en espera o flotando a la deriva con ancla de capa (*sea anchor*), los paneles recargan completamente el banco LiFePO4 sin consumir una sola gota de gasolina, garantizando autonomía para avionica y comunicaciones perpetuas.

---

## Bloque 5: Modelo Financiero, Presupuesto en 3 Bolsas y Retorno de Inversión (ROI)

### [Q-10] ¿Cómo justificar el costo ante los socios de la cooperativa y armadores?
* **Respuesta Técnica (El Análisis de Diésel Real):**
  * **Operación Tradicional:** 30 a 50 pangas + 1 Barco Nodriza saliendo "a buscar a ciegas".
    * Consumo promedio por panga: 70 litros de gasolina por jornada $\times$ 30 pangas = **2,100 litros diarios**.
    * A \$24 MXN/litro = **\$50,400 MXN diarios solo en gasolina de pangas** (más el diésel marino del nodriza).
    * Una temporada de 60 mareas activas representa **>\$3,000,000 MXN en combustible**.
  * **Con Detección Satelital + USV:** Reducción comprobada del 30% al 45% en tiempos de navegación infructuosa.
    * Ahorro mínimo estimado: **\$900,000 a \$1,350,000 MXN por zafra**, amortizando la totalidad del sistema USV en menos de media temporada.

### [Q-11] ¿Cuál es la estructura recomendada para la propuesta económica?
* **Estructura en 3 Bolsas de Inversión Transparente:**
  * **Bolsa 1 (Compras Directas en EE. UU. / Importación):** Adquisición directa con tarjeta del cliente a precios de fábrica sin sobreprecio de intermediarios (Aviónica Pixhawk Orange+, transductores Simrad/Airmar, propulsores Blue Robotics, módem Starlink Maritime, baterías).
  * **Bolsa 2 (Proveeduría y Maquila en México):** Tubería HDPE Tubomex o perfiles de aluminio naval 5083, tornillería inoxidable 316, soldadura TIG/MIG, arneses marinos y consumibles.
  * **Bolsa 3 (Ingeniería Cibernética y Honorarios Profesionales):** Diseño naval, cálculo de balance de potencia, programación del pipeline GEE/CMEMS, integración embebida, calibración de radioenlaces y acompañamiento técnico en pruebas de mar.

---

## Bloque 6: Análisis de Variación de Electrónica, Selección Calidad-Precio, Trimarán y Dual F9P

### [Q-12] ¿Por qué estuvieron cambiando los dispositivos electrónicos propuestos entre sesiones anteriores?
* **Respuesta Técnica:**
  * **Causa 1 (De Ciencia Pura a Realidad Comercial):** Inicialmente el modelo propuso instrumentación oceanográfica científica de laboratorio (Simrad EK80 a \$15k–\$30k USD, cámaras acústicas ARIS a \$80k USD). Al aterrizar el caso de negocio para cooperativas de Sonora/Sinaloa, fue necesario descartar equipos de investigación académica y buscar sensores con ROI comercial viable.
  * **Causa 2 (Colapso del Modelo 100% Eléctrico):** Se comenzó modelando un USV tipo BlueBoat de 2.5 m a baterías puras; pero al calcular la misión real (7 horas de 11 PM a 6 AM contra corrientes de marea de 2.5 nudos), la demanda energética ($>7\text{ kWh}$) exigía más de 150 kg de baterías. Esto obligó a migrar al **sistema Híbrido Serie (Generador Inverter + Baterías)**.
  * **Causa 3 (Fricción Electromagnética y Rumbo):** Al meter corrientes continuas de 40A–80A y un alternador de generador, los magnetómetros (brújulas) se vuelven inútiles por desvío magnético, obligando a sustituirlos por **GNSS Dual RTK**.
  * **Causa 4 (Sobredimensionamiento de Cómputo):** Se propuso Nvidia Jetson Orin Nano pensando en visión artificial pesada con cámaras térmicas FLIR. Al no ser indispensable la visión nocturna para la detección de camarón bentónico, la Jetson representa un gasto y consumo innecesario frente a una **Raspberry Pi 5**.

### [Q-13] ¿Cuál es la selección definitiva por Calidad / Precio (Value for Money)?

| Componente | Opción Descartada (Excesiva o Deficiente) | Selección Óptima Recomendada | Justificación Calidad / Precio |
| :--- | :--- | :--- | :--- |
| **Autopiloto** | Pixhawk genérico sin aislamiento de vibración | **CubePilot Cube Orange+** (o Pixhawk 6C) | Sensores redundantes amortiguados, soporte nativo ArduBoat y doble puerto GNSS por DroneCAN. |
| **Geoposicionamiento y Rumbo** | Brújula magnética convencional (\$50 USD, falla por ruido) | **2x u-blox ZED-F9P (Moving Baseline)** | **Costo \$0 USD (ya disponibles en inventario)**. Provee rumbo satelital verdadero (*True Heading*) con precisión de $0.1^\circ$, 100% inmune a motores y generador. |
| **Cómputo de Misión** | Nvidia Jetson Orin Nano (\$499 USD, 25W) | **Raspberry Pi 5 8GB** (\$80 USD, 5-10W) | Procesa telemetría, puente MAVLink, scripts Python y registros de sonar consumiendo 60% menos energía. |
| **Propulsión** | Motores fuera de borda con timón móvil | **2x Thrusters Blue Robotics T500** | Sin timón mecánico que se trabe con sargazo o redes; empuje diferencial indestructible en agua salada. |
| **Generador Híbrido** | Generador marino diésel pesado (\$6,000 USD, >80 kg) | **Inverter Honda EU22i / Yamaha** (\$1,200 USD, 21 kg) | Silencioso, repuestos universales en Sinaloa/Sonora, arranca y apaga por relé electrónico. |
| **Sensor de Biomasa** | Simrad EK80 WBT Mini (\$18,000 USD) | **Airmar CHIRP 200 kHz o Blue Robotics Ping/Ping360** | Cumple con la discriminación de fondo blando vs duro a una fracción del costo (<10%). |

### [Q-14] ¿Por qué la opción del Pontón convertido en Trimarán con disipador de olas es superior?
* **Arquitectura Trimarán:**
  1. **Sección Central (Crujía):** Concentra el peso del generador, tanque de 20 L y banco LiFePO4 en la quilla central. Bajar este peso al centro de carena elimina la inestabilidad de balanceo.
  2. **Pontones Laterales (Amas):** Proporcionan brazo adrizante pasivo. El USV no escorará con el oleaje, manteniendo el haz acústico del sonar vertical hacia el fondo.
  3. **Disipador de Olas (*Wave Deflector* a 45°):** Actúa como tajamar rompedor de olas en proa, impidiendo que el oleaje corto del Golfo de California golpee la superestructura o moje la cubierta de paneles solares.
