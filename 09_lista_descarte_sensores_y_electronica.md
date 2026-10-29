# 09. Matriz de Selección Tecnológica: MVP de Bajo Costo vs. Grado Científico (Camarón, Pescado y Jaiba)

## Metadata de Control
* **Proyecto:** Plataforma Satelital 3m y USV Trimarán Híbrido 48V "Stealth" (Golfo de California: Topolobampo–Ohuira–Santa María y Bahía de Kino).
* **Propósito:** Definir qué sensores quedan **desbloqueados** al incorporar la prospección de **Jaiba (*Callinectes bellicosus* / *C. arcuatus*)** junto a **Camarón** y **Pescado (Escama/Sardina)**, estructurando dos arquitecturas comerciales: **1) MVP de Bajo Costo (Cooperativas)** y **2) Grado Científico (INAPESCA / CIBNOR / Certificación Acústica)**.

---

## 1. Sensores Desbloqueados (Actualización por Requerimiento de Jaiba + Escama + Camarón)

La incorporación de **Jaiba** exige evaluar la interfase agua-sedimento ($0\text{ a }10\text{ cm}$ del fondo), el micro-relieve bentónico (conchal, ecótono arena-lodo, pasto marino *Zostera*) y el oxígeno disuelto de fondo ($DO$) para evitar mortalidad en trampas. Por ello, **se desbloquean los siguientes equipos divididos en dos niveles de inversión**:

| Subsistema / Función | Opción A: MVP de Bajo Costo (Rigor Comercial Cooperativas) | Opción B: Grado Científico (Estándar Oceanográfico INAPESCA / CIBNOR) | Especie Principal Beneficiada |
| :--- | :--- | :--- | :--- |
| **1. Sonar Acústico Nadir (Columna y Fondo)** | **Garmin GSD 25 + Airmar B265LH CHIRP Dual (50/200 kHz, 1 kW)** (\$2,600 USD). Discrimina lodo blando (200 kHz) y cardúmenes profundos (50 kHz). | **Simrad EK80 WBT Mini Scientific Echosounder (70/120/200/333 kHz)** (\$22,500 USD). Inversión acústica multifrecuencia calibrada con esfera de carburo de tungsteno para biomasa absoluta ($g/m^3$). | **Camarón, Pescado y Jaiba** |
| **2. Sonar de Barrido Lateral / Imagen Acústica Bentónica** *(Desbloqueado para Jaiba)* | **Garmin GT56UHD-TM SideVü/ClearVü (455/800/1000 kHz)** o **Cerulean Omniscan 450 SS** (\$550 – \$1,450 USD). Barre 30–50 m por banda, detecta ecótonos lodo-conchal, depresiones de forrajeo y trampas fantasma. | **Cámara Acústica Multihaz Blueprint Subsea Oculus M1200d (1.2 MHz / 2.1 MHz)** o **Edgetech 4125i Side-Scan** (\$28,000 – \$42,000 USD). Visión acústica milimétrica en turbidez cero-luz. | **Jaiba (*Callinectes spp.*)** y Bentos |
| **3. Perfilador Fisicoquímico y Oxígeno Disuelto ($DO$) de Fondo** *(Desbloqueado para Jaiba)* | **Turner Cyclops-7F (Clorofila/Turbidez) + Sonda Óptica Industrial Atlas Scientific EZO-DO + Micro-CTD** (\$3,650 USD total). Previene calar trampas en bolsas hipóxicas ($DO < 2.2\text{ mg/L}$). | **RBRconcerto³ C.T.D.DO.Chl.Turb** o **Sea-Bird SBE 19plus V2 SeaCAT** (\$14,500 – \$19,000 USD). Precisión metrológica de $\pm 0.002^\circ\text{C}$ y $\pm 0.003\text{ mS/cm}$. | **Jaiba** (Anti-hipoxia en nasas), **Camarón** y **Pescado** |
| **4. Acústica Pasiva Submarina (Hidrófono)** | **Aquarian H3d-Ethernet Digital Hydrophone** (\$1,900 USD) con clasificación DSP en Jetson: filtra roca en camarón ($>2.4\text{ kHz}$), detecta trituración de bivalvos por quelas de jaiba ($1.2\text{--}3.5\text{ kHz}$) y coro de curvina ($450\text{ Hz}$). | **IcListen Smart Hydrophone HF (Ocean Sonics, 10 Hz – 200 kHz)** (\$9,800 USD). Calibrado en dB re $1\ \mu\text{Pa}$ con espectrograma direccional. | **Jaiba, Curvina y Exclusión Roca** |
| **5. Visión Submarina y Superficial Edge AI** | **FLIR Boson 320 (Superficie) + Cámara Quilla Blue Robotics Low-Light HD USB con LED Ámbar** (\$2,690 USD) corriendo YOLOv8-Nano en **NVIDIA Jetson Orin Nano (67 TOPS)**. | **FLIR Boson 640 Radiométrica + Sistema Estéreo Submarino Calibrado ZED X / SubC Imaging** (\$8,900 USD) en **NVIDIA Jetson AGX Orin Industrial (275 TOPS)**. | **Jaiba** (Conteo visual aguas claras <4 bz) y Seguridad |
| **6. Ingesta Satelital Multiespectral** | **Sentinel-2 (10m) + VIIRS SST + Copernicus CMEMS (\$0 USD/mes)** + **PlanetScope 3m en Modo Trial / Polígono Focal (\$600 USD/mes)**. | **PlanetScope SuperDove 8-Bandas 3.0m Diario + Tasking Satelital SAR Capella/ICEYE** (\$2,500 – \$4,500 USD/mes). | **Camarón, Pescado y Jaiba** |

---

## 2. Componentes Permanentemente Descartados (Por Seguridad e Ingeniería Naval)

Aunque se desbloquearon los sensores acústicos y ópticos para el doble nivel (**MVP Bajo Costo** vs. **Grado Científico**), los siguientes elementos **permanecen estrictamente prohibidos** en ambas versiones por física marina:

1. **Brújulas Magnéticas Convencionales (I2C/SPI HMC5883 / IST8310):**
   * **Causa:** Los 80A–125A DC del bus de 48V y el alternador desvían el rumbo magnético provocando giros erráticos (*toiletbowling*).
   * **Estándar Inamovible:** **Dual u-blox ZED-F9P en Moving Baseline** ($0.1^\circ$ de rumbo verdadero satelital).
2. **Timones Mecánicos Expuestos con Servos:**
   * **Causa:** Se traban con cabos de boyas jaiberas, sargazo y bolsas plásticas.
   * **Estándar Inamovible:** **Empuje Diferencial (*Skid-Steering*)** con pods de 48V protegidos por toberas Kort corta-cabos.
3. **Paneles Solares de Vidrio en Cubierta:**
   * **Causa:** Fragilidad ante impacto de ola en barra, peso alto sobre metacentro y atractivo visual para robo nocturno.
   * **Estándar Inamovible:** **Cubierta Ciega "Stealth"** con planta híbrida 4T + banco masivo LiFePO4 48V 200Ah (10.24 kWh, 25 MN *Limp-Home*).
4. **Muestreadores de ADN Ambiental (eDNA) en Línea:**
   * **Causa:** Latencia de laboratorio de 6 a 12 horas; incapaz de guiar el calado táctico de trampas o redes antes del amanecer.
