# 09. Lista de Descarte de Sensores, Electrónica y Arquitecturas Navales

## Metadata de Control
* **Proyecto:** Trimarán Híbrido de Prospección USV para Pesca de Camarón (Golfo de California).
* **Propósito:** Registro formal y exhaustivo de todos los sensores, componentes electrónicos, materiales de casco y métodos descartados durante el proceso de ingeniería, detallando la justificación técnica, física, biológica y económica.
* **Función para NotebookLM:** Evitar que el sistema vuelva a sugerir o indagar sobre tecnologías incompatibles con la realidad operativa de Sonora/Sinaloa.

---

## 1. Matriz General de Equipos y Sensores Descartados

| Dispositivo / Tecnología | Costo Aprox. | Razón Principal de Descarte | Sustituto Adoptado |
| :--- | :--- | :--- | :--- |
| **Simrad EK80 WBT Mini** | \$18,000 – \$25,000 USD | Costo prohibitivo para cooperativas; excesivo para solo clasificar dureza de fondo. | **Airmar CHIRP 200 kHz / Blue Robotics Ping360** (<10% del costo). |
| **Cámara Acústica ARIS / Oculus** | \$35,000 – \$80,000 USD | Requiere AUV/ROV a 1 m del fondo; inviable para escaneo superficial de gran área. | Validación indirecta (Sondeo de lecho blando + pluma de turbidez). |
| **Muestreador Robótico de eDNA** | \$15,000 – \$40,000 USD | Análisis molecular lento; no entrega datos en tiempo real antes de las 05:30 AM. | Modelo estuarino GEE + Sonar de fondo. |
| **Cámara Térmica FLIR Boson** | \$3,500 – \$6,000 USD | El camarón es bentónico (sumergido a 10-30 m); la visión superficial no lo detecta. | Cero cámaras térmicas; navegación por waypoints GNSS geocercados. |
| **Radar Marino 24 GHz** | \$2,200 – \$4,500 USD | Consumo eléctrico elevado (30W-50W); la evasión en altamar se resuelve por geocerca. | Transpondedor AIS clase B pasivo + luces de navegación reglamentarias. |
| **Nvidia Jetson Orin Nano** | \$499 USD + periferia | Consumo de 25W; procesamiento de IA no requerido si no hay visión artificial activa. | **Raspberry Pi 5 (8GB)** (5W–10W, \$80 USD). |
| **Hidrófono Pasivo para Clics** | \$2,500 – \$8,000 USD | El camarón comercial casi no produce sonido en mar abierto sobre lodo; snapping shrimp engaña. | Hidrófono básico solo como filtro para descartar roca; no para rastreo. |
| **Banco Baterías 100% Eléctrico** | \$6,500 – \$9,000 USD | Peso masivo (>150 kg) para cubrir 7 horas continuas contra 2.5 nudos de corriente. | **Híbrido Serie:** Generador Inverter Honda EU22i (21 kg) + LiFePO4 buffer. |
| **Brújulas Magnéticas (I2C/SPI)** | \$50 – \$150 USD | Campos de 40A–80A DC y alternador de generador corrompen el rumbo magnético. | **Dual u-blox ZED-F9P (Moving Baseline)**: True Yaw satelital a 0.1°. |
| **Timones Mecánicos con Servos** | \$300 – \$600 USD | Se traban la primera noche con sargazo, bolsas plásticas y cabos de redes. | **Empuje Diferencial (*Skid-Steering*)** con 2x thrusters T500 sin partes móviles expuestas. |
| **Casco 2.5m de Fibra Monocasco** | \$4,500 USD | Poca manga; balancea el haz del sonar con oleaje; sin espacio para generador ni tanque. | **Pontón Recreativo Trimarán** con flotadores de aluminio y tanque integrado. |
| **Relleno con Espuma Poliuretano** | \$800 USD | Absorbe agua de mar por delaminación con el tiempo, añadiendo hasta 40% de peso muerto. | **Mamparas Interiores Estancas Herméticas** con válvulas de purga. |
| **Software Comercial (Zunibal/CatSat)** | \$10,000 – \$25,000 USD/año | Píxeles ciegos de 1 a 4 km en la franja costera de 2 a 15 brazas (bocas de esteros). | **Pipeline propio GEE (Sentinel-2 a 10m)** + CMEMS a \$0 USD. |
| **Panga Rápida / Wave Runner** | \$12,000 – \$18,000 USD | Gasta 60-80 L de gasolina por salida; arriesga tripulación humana de madrugada. | **USV Autónomo Híbrido no tripulado** (gasta ~3 L por noche). |

---

## 2. Justificación Técnica Detallada por Componente

### 1. Ecosonda Científica Simrad EK80 WBT Mini (\$18,000 - \$25,000 USD)
* **Por qué se evaluó:** Es el estándar de oro oceanográfico mundial para cuantificar biomasa de organismos sin vejiga natatoria como el krill y camarón mediante inversión multifrecuencia (120, 200, 333 kHz).
* **Por qué se descarta:**
  * **Económico:** Representa por sí sola más del 60% del costo total del USV, haciendo que el proyecto sea inviable para la aprobación de la mesa directiva de las cooperativas.
  * **Operativo:** Requiere calibración con esferas de carburo de tungsteno suspendidas y un oceanógrafo procesando ecogramas en Echoview.
* **Sustituto:** Un transductor **Airmar CHIRP 200 kHz** o un **Blue Robotics Ping Sonar / Ping360** (\$350 - \$2,500 USD). Para pesca comercial artesanal, no se requiere calcular gramos de biomasa por metro cúbico exactos; basta con discriminar si el fondo es fango suave (donde está el camarón) vs. arena dura o piedra.

---

### 2. Cámara Acústica ARIS / Blueprint Subsea Oculus (\$35,000 - \$80,000 USD)
* **Por qué se evaluó:** Permite "ver siluetas de camarones" en agua con turbidez severa usando frecuencias de 1.2 a 3.0 MHz.
* **Por qué se descarta:**
  * **Física Acústica:** A 3.0 MHz la absorción acústica es tan alta que el alcance máximo es de apenas 2 a 5 metros.
  * Para que funcione, el sonar debe estar a 1 metro del lecho marino montado en un micro-AUV o sled remolcado, lo cual en aguas someras con corrientes y redes es una receta para el enredo y pérdida del equipo.
* **Sustituto:** Detección de macro-hábitat (correlación de turbidez estuarina satelital + ecotono de lodo de fondo).

---

### 3. Muestreadores Robóticos de ADN Ambiental (eDNA) (\$15,000 - \$40,000 USD)
* **Por qué se evaluó:** Certeza biológica del 99% mediante detección de células y exoesqueletos de camarón café/azul.
* **Por qué se descarta:**
  * **Tiempo de Respuesta:** El proceso de filtrado de agua, lisis celular, amplificación qPCR o secuenciación portátil toma entre 4 y 12 horas.
  * La ventana crítica exige entregar las coordenadas al Capitán del Barco Nodriza **antes de las 05:30 AM**. El eDNA no ofrece inmediatez táctica diaria.

---

### 4. Computadora de Borde Nvidia Jetson Orin Nano Super (\$499 USD)
* **Por qué se evaluó:** Inferencia de redes neuronales (YOLOv8) para detección de obstáculos con cámaras ópticas y térmicas.
* **Por qué se descarta:**
  * **Balance de Potencia:** Consume entre 15W y 25W de forma sostenida, requiriendo convertidores DC-DC pesados y disipación activa.
  * Al navegar en altamar de noche por rutas preprogramadas con geocercas satelitales y luces reglamentarias, no se requiere visión computacional intensiva a bordo.
* **Sustituto:** **Raspberry Pi 5 (8GB)** (\$80 USD, consumo de 5W–10W), perfecta para correr Linux, ROS2 básico, bridge MAVLink, scripts de telemetría LoRa y filtrado de datos de sonar.

---

### 5. Sensores de Rumbo Magnéticos / Brújulas Digitales (\$50 - \$150 USD)
* **Por qué se evaluó:** Son las brújulas convencionales de los kits de autopiloto (IST8310, HMC5883L).
* **Por qué se descarta:**
  * **Falla Crítica de Navegación:** El tren motriz del USV maneja corrientes de 40A a 80A DC en los cables de potencia, sumado al campo electromagnético del alternador del generador inverter. Esto produce un desvío magnético dinámico que vuelve loco al filtro EKF de ArduPilot, haciendo que el barco navegue en círculos (*toiletbowling*).
* **Sustituto:** **Dual u-blox ZED-F9P (Moving Baseline)** ya disponibles por el consultor. Al calcular el rumbo por diferencia de fase portadora GNSS entre dos antenas (proa y popa), el rumbo es 100% satelital y totalmente inmune a interferencias electromagnéticas.

---

### 6. Casco Monocasco o Catamarán Ligero de 2.5 metros (\$4,500 USD)
* **Por qué se evaluó:** Facilidad de transporte y botadura manual rápida.
* **Por qué se descarta:**
  * **Resistencia al Mar:** En el Golfo de California el viento genera olas picadas de 0.8 a 1.2 m (Beaufort 3-4); un barco de 2.5 m sufre cabeceo excesivo que saca el sonar del agua.
  * **Falta de Volumen:** No tiene espacio de cubierta para montar 6 paneles solares de tamaño estándar ni volumen en sentina para un generador de 21 kg y tanque de combustible.
* **Sustituto:** **Pontón Recreativo de Aluminio convertido en Trimarán con pontón central**:
  * Ofrece flotabilidad masiva, estabilidad anti-rolido para el sonar y **ya incluye de fábrica el tanque marino de combustible de 90 a 150 litros**, resolviendo la autonomía por completo sin fabricar un tanque especial.

---

### 7. Relleno con Espuma de Poliuretano en los Flotadores
* **Por qué se evaluó:** Tradicionalmente se inyecta espuma en embarcaciones menores para certificar inhundibilidad.
* **Por qué se descarta:**
  * En ambientes marinos con vibración continua, la espuma sufre micro-fisuras y absorbe salmuera por capilaridad.
  * En 1 o 2 zafras, el casco absorbe entre 30 y 60 litros de agua salada retenida en la espuma que no se puede drenar, incrementando el calado y arruinando el consumo de combustible.
* **Sustituto:** **Mamparas interiores herméticas soldadas** dividiendo cada flotador en compartimentos estancos independientes con válvulas de purga y registro de presión.
