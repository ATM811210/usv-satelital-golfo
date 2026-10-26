# CONTEXTO MAESTRO DEL PROYECTO: ANALÍTICA SATELITAL Y TRIMARÁN USV MULTIESPECIE (48V "STEALTH")
*Documento Consolidado de Alta Densidad para Ingesta en Modelos de Razonamiento (Argon) - Temperatura recomendada: 0.2*

---

## 1. Misión, Operación y Estrategia Comercial de Doble Turno
* **Objetivo:** Optimizar la pesca industrial y cooperativa en el Golfo de California (Topolobampo $\leftrightarrow$ Bahía de Kino) eliminando la prospección empírica.
* **Estrategia en Dos Fases:**
  * **Semana 3 (Día 21) - Satélite Diario PlanetScope 3 m:** Antes de que el USV entre al agua, se activa la plataforma web con fotos diarias de 3 metros y capas térmicas VIIRS/GOES. Las pangas reciben a las 10:00 PM las coordenadas exactas de las plumas de turbidez. Costo: **$3,600 USD por 6 meses ($600 USD/mes)**.
  * **Semana 8 - Trimarán Híbrido Multiespecie 48V:**
    * *Turno Noche (Camarón: 11 PM a 5 AM):* Barrido a 200 kHz en fondos someros (2 a 15 brazas). Despacho a pangueros antes de las 5:30 AM.
    * *Turno Día (Sardina y Escama: 5:30 AM a 12 PM):* Conmutación a 50 kHz y sensor óptico de clorofila para cardúmenes de sardina monterrey, crinuda, macarela y frentes de medusa/curvina en mar abierto.

---

## 2. Arquitectura Naval y Casco
* **Diseño "Stealth" Antirrobo:** Cero paneles solares en cubierta (evita reflejos visibles a kilómetros en Sinaloa/Sonora y baja resistencia al viento en tormentas Beaufort 6). Cubierta plana de aluminio gris mate con aspecto de balsa pesada.
* **Opciones de Casco Evaluadas:**
  * **Opción 1: Trimarán de Aluminio 5083 Fabricado desde Cero:** **$5,600 USD** (Quilla central en V profunda + flotadores + tanque 60 L con snorkel).
  * **Opción 2: Pontón Recreativo Usado ($45,000 MXN base) Modificado:** **$4,425 USD total ($88,500 MXN)**. Base usada ($45k MXN) con tanque marino integrado de 90–150 L + pontón central de aluminio ($18k MXN) + tajamar disipador de olas a 45° ($8k MXN) + soportes de popa y cajas ($17.5k MXN).
  * **Opciones Comerciales (OceanAlpha / Otter Pro):** >$75,000 a $85,000 USD landed en México (descartadas por costo, hélices expuestas y nula hibridación).

---

## 3. Tren Motriz de Alta Potencia (48V) y Respaldo Masivo LiFePO4
* **Propulsión:** **2x Pods Submarinos Brushless de 3.0 kW (48V)** (~10-12 HP hidrodinámicos) con toberas corta-cabos.
  * Velocidad de tránsito: **10 a 12 nudos** (llega al polígono en la mitad de tiempo).
  * Velocidad de escaneo: 3 nudos en modo silencioso.
* **Planta Híbrida 4T Automatizada:** Motor térmico con generador 48V (3.5 kW) con arranque eléctrico gobernado por relé.
* **Banco Masivo LiFePO4 Doble Respaldo (10.24 kWh - 48V 200Ah + BMS):**
  * **Capacidad Limp-Home:** Si el generador falla a **20 millas náuticas** de Topolobampo a las 3:00 AM, las baterías garantizan **25 millas de regreso** a 4.5 nudos en modo 100% eléctrico, evitando que el USV quede a la deriva con equipo de alto valor.

---

## 4. Aviónica, Cómputo y Seguridad Legal
* **Autopiloto:** CubePilot The Cube Orange+ Standard Set con triple IMU amortiguada corriendo ArduPilot (ArduBoat).
* **Geoposicionamiento y Rumbo Verdadero:** **Dual u-blox ZED-F9P RTK (Moving Baseline)** del consultor (**$800 USD**) calculando True Yaw a 0.1° sin desvío magnético.
* **Computadora de Misión:** **NVIDIA Jetson Orin Nano Super (8GB, 67 TOPS)** + NVMe 1TB Industrial (fusión de datos, ROS2 y telemetría).
* **Seguridad y Visión:** Cámara térmica FLIR Boson + Transpondedor AIS Clase B homologado ante SEMAR + Luces COLREG.
* **Comunicaciones:** Starlink Mini / Marítimo DC + Radioenlace RFDesign RFD900x (915 MHz).

---

## 5. Sensores Submarinos Multiespecie
* **Ecosonda CHIRP Doble Frecuencia (50 kHz / 200 kHz):** Airmar B75M / TM185 (Camarón a 200 kHz somero / Sardina a 50 kHz profundo hasta 250 m).
* **Minisonda CTD + Fluorómetro de Clorofila-a y Turbidez:** Turner Designs Cyclops-7F integrado en la quilla para frentes biológicos diurnos.
* **Hidrófono Pasivo:** Filtro de exclusión para descartar fondos rocosos con chasquidos de camarón pistola.

---

## 6. Cuadro Financiero Consolidado Llave en Mano ($54,320 USD)

| Rubro de Inversión | Descripción Técnica | Monto (USD) |
| :--- | :--- | :--- |
| **1. Casco Trimarán** | Aluminio 5083 + Tubos PAD con Espuma + Tanque 60L con Snorkel (*o Pontón Modificado*) | **\$5,600 USD** |
| **2. Propulsión Alta Potencia** | 2x Pods 3 kW 48V Brushless + Planta Híbrida 4T Automatizada | **\$4,400 USD** |
| **3. Banco Baterías Doble Respaldo** | 10.24 kWh LiFePO4 (48V 200Ah + Smart BMS 200A) con respaldo 25 millas | **\$2,650 USD** |
| **4. Aviónica, Cómputo y Legal** | Cube Orange+, Dual F9P RTK (\$800), Jetson, Starlink, FLIR Boson, AIS SEMAR | **\$8,250 USD** |
| **5. Sensores Submarinos** | CHIRP Dual 50/200 kHz + Hidrófono de descarte + CTD/Clorofila/Turbidez | **\$7,700 USD** |
| **6. Logística, Aduanas e Insumos** | Fletes Hazmat, aranceles (IVA/IGI), tornillería Inox 316, cables marinos AWG 2/0 y cajas IP68 | **\$5,720 USD** |
| **7. Satélite Diario PlanetScope** | Suscripción comercial diaria 3 m para Topolobampo / Ohuira (6 Meses a \$600/mes) | **\$3,600 USD** |
| **8. Ingeniería y Software** | Ingeniería naval, plataforma Web GIS satelital, orquestación n8n, gestoría SEMAR y ensamble | **\$16,400 USD** |
| **TOTAL LLAVE EN MANO (OPCIÓN A)** | **Trimarán Híbrido 48V Comercial Multiespecie Completo** | **\$54,320 USD** |
