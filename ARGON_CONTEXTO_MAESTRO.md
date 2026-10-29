# CONTEXTO MAESTRO DEL PROYECTO: ANALÍTICA SATELITAL 3M Y TRIMARÁN USV TRI-ESPECIE (48V "STEALTH")
*Documento Consolidado de Alta Densidad para Contexto de Ingeniería y Modelos Agénticos (SSOT)*

---

## 1. Misión, Operación y 3 Opciones de Prospección (Camarón, Pescado y Jaiba)
* **Objetivo:** Eliminar la prospección pesquera a ciegas en el Golfo de California (Topolobampo–Ohuira–Santa María, SIN $\leftrightarrow$ Bahía de Kino / Guaymas, SON) combinando satélites comerciales de **3.0 metros diarios (PlanetScope 8-Bandas)** con verificación in-situ mediante un **USV Trimarán Híbrido de 48V ("Stealth")**.
* **3 Opciones Operativas en Plataforma Web GIS y USV:**
  1. **Opción 1 — Camarón (`NOCTURNO_CAMARON`, 22:00 a 05:15 hrs):** Camarón azul (*L. stylirostris*) y café (*F. californiensis*) en canales de 2.0 a 12.5 brazas. Fusión de turbidez PlanetScope 3m ($\text{NDTI} \in [0.06, 0.22]$), ventana termohalina de fondo ($24.0^\circ\text{C}\text{--}28.5^\circ\text{C}$, $28\text{--}36\text{ PSU}$), sonar CHIRP a 200 kHz y exclusión acústica de roca rompe-redes ($>2.4\text{ kHz}$ en hidrófono).
  2. **Opción 2 — Pescado y Pelágicos (`DIURNO_SARDINA` / `PESCADO`, 05:30 a 12:00 hrs):** Sardina Monterrey, curvina golfina, pargo y aguamala en 10 a 90 brazas. Basado en frentes de Clorofila-a RedEdge ($>2.5\text{ mg/m}^3$), surgencia térmica ($17.5^\circ\text{C}\text{--}23.0^\circ\text{C}$), sonar CHIRP a 50 kHz (penetración 250 m) y detección hidrofónica de coros de curvina ($450\text{ Hz}$).
  3. **Opción 3 — Jaiba Bentónica (`PROSPECCION_JAIBA`, 0.8 a 8.5 brazas):** Jaiba café guerrera (*Callinectes bellicosus*) y jaiba azul (*Callinectes arcuatus*) para calado de trampas/nasas. Integra:
     - **Sonda Óptica de Oxígeno Disuelto ($DO$) en Fondo:** Bloquea el calado de trampas si $DO < 2.2\text{ mg/L}$ (evita mortandad por hipoxia estuarina dentro de la nasa; óptimo $\ge 3.2\text{ mg/L}$).
     - **Sonar de Barrido Lateral UHD (*Side-Scan* 455/800/1000 kHz o Cámara Acústica Oculus 1.2 MHz):** Resuelve la zona ciega del haz nadir identificando ecótonos arena-conchal, praderas de *Zostera* y trampas fantasma.
     - **Acústica Pasiva Trófica (`H3d` en banda 1.2–3.5 kHz):** Detecta el crujido de bivalvos/almejas triturados por quelas de jaiba en alimentación activa.

---

## 2. Fundamentos Físicos y Biológicos Clave (Destilados de Investigación)
* **Reflectancia Acústica sin Vejiga Natatoria:** Ni el camarón ni la jaiba poseen vejiga natatoria ($TS \approx -45\text{ a }-65\text{ dB}$). En el MVP Comercial se discrimina el hábitat por dureza/textura de sustrato (CHIRP 200 kHz + Side-Scan 800 kHz) y variables fisicoquímicas ($DO$, Temp, Salinidad, Turbidez); en el Grado Científico se cuantifica biomasa absoluta ($g/m^3$) mediante inversión multifrecuencia de banda ancha (**Simrad EK80 WBT Mini 70/120/200/333 kHz** calibrado con esfera de carburo de tungsteno) e imagen multihaz (**Blueprint Subsea Oculus M1200d**).
* **Dualidad del Hidrófono Submarino:** El chasquido de alta intensidad ($>2.4\text{ kHz}$) en mar abierto proviene de camarón pistola (*Alpheidae*) asociado a arrecife/piedra viva. Para redes de arrastre camaroneras es un **filtro estricto de exclusión rompe-redes**; para trampas fijas de jaiba, la banda de $1.2\text{ a }3.5\text{ kHz}$ sobre ecótono arena-conchal actúa como **indicador positivo de forrajeo**.
* **Inmunidad Electromagnética de Rumbo:** Los 80A–125A DC del bus de 48V y el alternador desvían cualquier brújula magnética hasta $35^\circ$. Es obligatorio usar **2x u-blox ZED-F9P en Moving Baseline** ($0.1^\circ$ True Yaw satelital).
* **Flotabilidad Positiva sin Absorción Salina:** Se priorizan mamparas estancas soldadas con purga e inyección controlada de celda cerrada, evitando poliuretano abierto que absorbe salmuera por delaminación.
* **Starlink Embarcado Indispensable:** El enlace **Starlink Mini DC (o Flat High Performance)** activo a bordo del USV es indispensable para transmitir ecogramas, mosaicos Side-Scan y alertas de hipoxia desde 25 MN mar adentro antes de que salgan las pangas, respaldado por radioenlace **RFD900x (915 MHz, 40+ km)**.

---

## 3. Tres Modalidades Comerciales y Presupuesto Auditado (Mano de Obra Separada)

| Modalidad | Alcance y Equipos Clave | Materiales / Equipos / Satélite | Mano de Obra (Astillero + Ingeniería Separada) | Total Llave en Mano (USD) |
| :--- | :--- | :---: | :---: | :---: |
| **1. Etapa 1 Independiente (`ETAPA_1_SATELITAL` — Día 21, Sin USV)** | Solo Análisis Satelital de Máxima Precisión (**PlanetScope 3.0m Diario 8-Bandas** + CMEMS Fondo $DO$/Temp/Sal + VIIRS + Sentinel-2 por 6 meses) + Cloud PostGIS/n8n + App Móvil Capitán Offline para **Camarón, Pescado y Jaiba**. | **\$4,320 USD** *(\$3,600 satélite 6m + \$720 cloud; o \$8,220 cobertura extendida)* | **\$6,800 USD** *(Ingeniería de Software Tri-Especie y App)* | **\$11,120 USD** *(Estándar)*<br/>**\$15,020 USD** *(Extendida)* |
| **2. MVP Comercial Trimarán 48V Completo (`MVP_BAJO_COSTO`)** | Materiales Navales Aluminio 5083 + 2x Pods 48V 3kW + LiFePO4 10.24 kWh (25 MN *Limp-Home*) + Generador 4T + Cube Orange+ + 2x RTK F9P + Jetson Orin Nano + FLIR Boson 320 + Radar 24GHz + AIS SEMAR (**\$17,429** con Pontón / **\$18,604** desde Cero) + **Starlink Mini Indispensable 6m + RFD900x (\$1,749)** + **Sensores 3 Especies: Garmin CHIRP + Side-Scan 800kHz + Turner CTD/Chl + Sonda DO + Hidrófono H3d (\$10,550)** + **Satélite 3m 6m (\$4,320)**. | **\$34,049 USD** *(con Pontón)*<br/>**\$35,224 USD** *(Casco Cero)* | **\$3,500 USD** *(Astillero TIG)*<br/>**+ \$16,400 USD** *(Ingeniería 4 Hitos)*<br/>**= \$19,900 USD** | **\$53,949 USD** *(con Pontón)*<br/>**\$55,124 USD** *(Casco Cero)* |
| **3. Grado Científico INAPESCA / CIBNOR (`GRADO_CIENTIFICO`)** | Trimarán 48V + Jetson AGX Orin 275 TOPS + FLIR 640 (**\$25,400**) + **Starlink Marítimo Prioritario (\$3,500)** + **Simrad EK80 WBT Mini + Cámara Acústica Oculus M1200d + Side-Scan Edgetech + RBRconcerto³ CTD-DO + icListen HF (\$78,400)** + **PlanetScope 3m Regional + Radar SAR (\$12,600)**. | **\$119,900 USD** | **\$4,500 USD** *(Astillero)*<br/>**+ \$24,000 USD** *(Ingeniería y Calibración Acústica)*<br/>**= \$28,500 USD** | **\$148,400 USD** |

---

## 4. Estado Actual de Avance de Ingeniería (MVP Web al 90.8% — 118 de 130 Horas Completadas, 100% Código/Docker)
* **Completado en Código, Base de Datos, Docker y Pruebas (`14 passed in 0.01s`):**
  * Motor matemático tri-especie (`engine_hsi.py`), conectores y datasets (`satellite_connectors.py`), API FastAPI (`main.py`), `Dockerfile`, `docker-compose.yml` (`postgis` + `backend_gis` + `n8n`), esquema espacial (`init_postgis.sql`), workflow tri-especie (`flujo_diario_10pm_y_5am.json`), controlador de misión Edge (`usv_mission_controller.py`), fusión de visión térmica y biomasa (`edge_vision_fusion.py`), portal interactivo (`index.html`) y CI/CD en GitHub Actions (`.github/workflows/ci.yml`).
* **Restante Operativo al Contratar Cliente (12 horas / ~1.5 días):** Insertar credenciales vivas de PlanetScope/CMEMS del cliente en `.env` (4h), vincular número de WhatsApp/Telegram en `n8n` (4h) y realizar prueba piloto en muelle con capitanes (4h).
