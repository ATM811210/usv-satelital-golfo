# 03. Especificaciones Formales de Hardware: Trimarán Híbrido 48V "Stealth"

## Metadata de Control
* **Plataforma Formal:** Trimarán Híbrido Serie de Alta Potencia (48V DC) - Arquitectura "Stealth" (Cero paneles solares en cubierta, perfil bajo antirrobo).
* **Velocidad de Misión:** Tránsito a **10–12 nudos** (2x Pods 3.0 kW) | Sondeo a 3 nudos.
* **Autonomía y Respaldo:** Tanque de combustible marino (60L a 100L) + **Banco Masivo LiFePO4 10.24 kWh (48V 200Ah)** con capacidad de retorno de emergencia (*Limp-Home*) de **25 millas náuticas** a 4.5 nudos si el generador térmico falla.

---

## 1. Tren Motriz de Alta Potencia y Planta Híbrida 48V

```
[ Tanque Combustible Marino (60L-100L) + Snorkel ] ──► [ Planta Generadora 4T Automatizada (3.5 kW / 48V) ]
                                                                      │ (Arranque eléctrico por relé)
                                                                      ▼
                                                       [ Banco Masivo LiFePO4 10.24 kWh ]
                                                       [   (48V 200Ah + Smart BMS)      ]
                                                                      │
                                                ┌─────────────────────┴─────────────────────┐
                                                ▼                                           ▼
                                 [ Pod Submarino Babor 3 kW ]                [ Pod Submarino Estribor 3 kW ]
                                 [     (48V Brushless)      ]                [       (48V Brushless)       ]
```

### Especificación de Potencia:
1. **Propulsión Principal:**
   * **2x Pods Submarinos Brushless de 3.0 kW (48V)** montados en popa con toberas de protección corta-cabos y anti-sargazo.
   * Empuje combinado equivalente a **~10–12 HP hidrodinámicos**.
   * Control por empuje diferencial (*skid-steering*) gestionado por ArduPilot (cero timones mecánicos expuestos).
2. **Planta Híbrida Térmica Automatizada:**
   * Motor de combustión 4T con generador DC 48V automatizado de 3.5 kW de salida continua.
   * Arranque eléctrico gobernado por relé desde el autopiloto (enciende al superar 5 nudos en tránsito y se apaga al entrar al polígono caliente para escaneo 100% silencioso).
3. **Banco de Baterías de Doble Respaldo (10.24 kWh LiFePO4 48V 200Ah):**
   * Configuración de celdas prismáticas LiFePO4 de grado automotriz / marino con Smart BMS Victron/JBD de 200A continuo.
   * **Seguridad Crítica Limp-Home:** Si el motor térmico falla a **20 millas náuticas** de Topolobampo a las 3:00 AM, las baterías garantizan **25 millas de navegación de regreso** a 4.5 nudos en modo 100% eléctrico, impidiendo que el USV quede a la deriva con equipo de alto valor.

---

## 2. Comparativa Presupuestal de Opciones de Casco

### Opción 1: Trimarán de Aluminio Naval 5083 Fabricado desde Cero (\$5,600 USD)
* Casco central en V profunda con flotadores laterales y tanque estructural de 60 L con snorkel anti-explosión.
* Manufactura en astillero local (Guaymas/Topolobampo) con 120 hrs de soldadura TIG naval calificada.

### Opción 2: Pontón Recreativo Usado (\$45,000 MXN) Modificado a Trimarán (\$4,425 USD / \$88,500 MXN)
* **Base:** Pontón recreativo usado de 18-20 pies (\$45,000 MXN) con sus 2 tubos de aluminio y tanque de fábrica integrado (90-150 L).
* **Modificaciones en taller:**
  1. Fabricación de pontón central en aluminio 5083 para alojar los 10.24 kWh y generador: \$18,000 MXN (\$900 USD).
  2. Tajamar disipador de olas (*Wave Deflector*) a $45^\circ$ en proa: \$8,000 MXN (\$400 USD).
  3. Adaptación de líneas de combustible del tanque de fábrica con trampa Racor: \$4,500 MXN (\$225 USD).
  4. Soportes de popa reforzados para los Pods de 3 kW a 48V con toberas: \$6,000 MXN (\$300 USD).
  5. Cajas estancas centrales y mamparas de cierre: \$7,000 MXN (\$350 USD).

### Opciones Comerciales de Catálogo (Para Comparativa con Clientes):
* **Opción 3 (OceanAlpha SL40 / M40):** \$45,000 USD EXW $\rightarrow$ **>\$75,000 USD puesto en México**. Solo batería (4-6 hrs), sin generador, casco frágil en marejada.
* **Opción 4 (Maritime Robotics Otter Pro / EchoBoat):** **>\$85,000 USD puesto en México**. Hélices expuestas, sin toberas corta-redes, costo inasumible para cooperativas.

---

## 3. Aviónica, Cómputo y Seguridad Legal (Bolsa 4: \$8,250 USD)

* **Piloto Automático:** CubePilot The Cube Orange+ Standard Set con Carrier Board y sensor de corriente de alta capacidad.
* **Geoposicionamiento y Rumbo Verdadero:** **Dual u-blox ZED-F9P RTK (Moving Baseline)** del consultor (\$800 USD) calculando True Yaw a 0.1° sin desvío magnético.
* **Computadora de Misión:** **NVIDIA Jetson Orin Nano Super (8GB, 67 TOPS)** + NVMe 1TB Industrial en caja disipadora húmeda de aluminio (interfase ROS2/MAVLink, fusión de datos de sonar y telemetría).
* **Visión Térmica y Seguridad Nocturna:** Cámara Térmica FLIR Boson 320/640 para detección de pangas sin luces y boyas flotantes.
* **Seguridad Marítima Oficial:** Transpondedor AIS Clase B marino homologado ante SEMAR y Capitanía de Puerto + luces de navegación COLREG estancas.
* **Comunicaciones:** Starlink Mini / Marítimo DC + Radioenlace RFDesign RFD900x (915 MHz).

---

## 4. Paquete de Sensores Submarinos Tri-Especie (Camarón, Pescado y Jaiba) — Dos Configuraciones

### Configuración A: MVP de Bajo Costo / Cooperativas (\$8,770 USD)
1. **Ecosonda Nadir CHIRP Dual (50 kHz / 200 kHz — Garmin GSD 25 + Airmar B265LH):**
   * **Modo Camarón (Noche):** 200 kHz para discriminación de fango orgánico suave en 2 a 12.5 brazas.
   * **Modo Pescado / Pelágicos (Día):** Conmutación a 50 kHz para cardúmenes de sardina, curvina y pargo (10 a 90 brazas).
2. **Sonar de Barrido Lateral UHD para Jaiba (*Side-Scan* 455/800/1000 kHz — Garmin GT56UHD / Cerulean Omniscan 450):**
   * Escaneo transversal de 30 a 50 m por banda en aguas someras (0.8 a 8.5 brazas) para mapear ecótonos arena-lodo, conchal, praderas de *Zostera* y localizar trampas jaiberas fantasma.
3. **Sonda Fisicoquímica de Fondo: Turner Cyclops-7F (Clorofila-a / Turbidez) + Sonda Óptica Oxígeno Disuelto (Atlas EZO-DO) + Micro-CTD:**
   * Mide fitoplancton (sardina/pescado), temperatura/salinidad de fondo (camarón/jaiba) y **Oxígeno Disuelto ($DO \ge 3.0\text{ mg/L}$)** para evitar calar trampas jaiberas en zonas de hipoxia estuarina.
4. **Hidrófono Digital Pasivo (`Aquarian H3d-Ethernet`) + Cámara Quilla Low-Light HD con LED Ámbar:**
   * Procesamiento DSP en Jetson Orin Nano: descarta fondos rocosos en arrastre camaronero ($>2.4\text{ kHz}$), detecta actividad trófica de quelas de jaiba triturando bivalvos ($1.2\text{--}3.5\text{ kHz}$) y coros de curvina ($450\text{ Hz}$).

### Configuración B: Grado Científico / Certificación Oceanográfica INAPESCA-CIBNOR (\$78,400 USD en Sensores)
1. **Ecosonda Científica Multifrecuencia Simrad EK80 WBT Mini (70/120/200/333 kHz):** Cuantificación absoluta de biomasa ($g/m^3$) calibrada con esfera de carburo de tungsteno.
2. **Cámara Acústica Multihaz Blueprint Subsea Oculus M1200d (1.2 / 2.1 MHz) + Side-Scan Edgetech 4125i:** Imagen acústica de alta resolución para conteo individual de jaiba y camarón en turbidez extrema.
3. **Perfilador Multiparamétrico RBRconcerto³ C.T.D.DO.Chl.Turb:** Estándar metrológico internacional ($\pm 0.002^\circ\text{C}$, $\pm 0.003\text{ mS/cm}$, optodo rápido de $O_2$).
4. **Hidrófono Calibrado Ocean Sonics icListen HF (10 Hz – 200 kHz) + Computadora NVIDIA Jetson AGX Orin Industrial (275 TOPS).**

---

## 5. Cableado Náutico, Cajas IP68 y Protecciones Eléctricas

* **Cableado de Potencia DC 48V:** Cable marino de cobre estañado AWG 2/0 (banco de baterías y generador) y AWG 4 estañado (pods de 3 kW), resistente a aceite, calor e hidrocarburos (UL 1426 Marine Standard).
* **Cajas de Conexión y Protección:**
  * Gabinetes principales de aluminio fundido anodizado con grado de protección **IP68** y juntas tóricas de neopreno.
  * Penetradores pasacascos submarinos tipo **Blue Robotics WetLink** y conectores circulares marinos roscados tipo M12/M16 IP68.
* **Protección Eléctrica:**
  * Fusibles marinos ANL sellados para 150A/200A en línea principal de 48V.
  * Desconectores de batería bipolares marinos Blue Sea Systems con bloqueo de seguridad.
  * Contactores de potencia de estado sólido de 48V gobernados por el BMS para corte por baja tensión / sobretemperatura.
  * Filtros de ferrita y supresores de transitorios (TVS) en líneas de datos para aislar la Jetson y Cube Orange+ del ruido del generador.
