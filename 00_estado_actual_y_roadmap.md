# 00. Estado Actual del Proyecto y Roadmap de Ingeniería (Línea Base Congelada)

## Resumen Ejecutivo de Una Página (SSOT / Context Primer)
* **Proyecto:** Plataforma Satelital Comercial Diaria (3 m) y Vehículo Autónomo de Superficie (USV Trimarán Híbrido 48V "Stealth") para Prospección Pesquera en Doble Turno (24h: Camarón de Noche + Sardina/Curvina/Aguamala de Día).
* **Zona Geográfica:** Golfo de California (Sistema Lagunar Topolobampo–Ohuira–Santa María, SIN $\leftrightarrow$ Bahía de Kino / Guaymas, SON).
* **Director de Ingeniería:** Ingeniero en Cibernética y Electrónica.
* **Cliente / Usuario Final:** Socios Inversionistas y Alianza de Cooperativas Pesqueras (flota >50 pangas camaroneras + renta diurna a barcos sardineros/escameros).
* **Estado Actual:** **Línea Base de Hardware y Presupuesto Congelada (Zero Component Drift)**; Entregable Ejecutivo para Clientes y Plan de Programación Web GIS (Hito Día 21) completados.

---

## Índice Maestro de la Documentación en `/Users/topete/Desktop/catamaran/`

| Archivo | Propósito Principal | Estado |
| :--- | :--- | :--- |
| **`ARGON_CONTEXTO_MAESTRO.md`** | Manifiesto maestro unificado de contexto rápido para Gemini Argon. | **Activo (SSOT)** |
| **`00_estado_actual_y_roadmap.md`** | Snapshot compacto y tabla de control de todos los documentos del proyecto. | **Actualizado** |
| **`01_contexto_y_arquitectura.md`** | Fundamentos de negocio, perfil operativo y restricciones del Golfo de California. | Completo |
| **`02_bitacora_investigacion.md`** | Matriz de subsistemas y Registro de Decisiones de Arquitectura (ADR-001 a ADR-007). | Completo |
| **`03_especificaciones_hardware_usv.md`** | **Línea Base Congelada de Hardware:** Propulsión 48V 6kW, Baterías LiFePO4 10.24 kWh, Cajas IP68, Cableado UL1426, 4 Cascos y BOM EE. UU. | **Congelado (Oficial)** |
| **`04_comunicaciones_y_telemetria.md`** | Starlink Mini, RFD900x (915 MHz 40+ km), Transponder AIS Clase B SEMAR y tramas NMEA/KML. | Completo |
| **`05_pipeline_datos_y_algoritmos.md`** | Fusión satelital diaria (**PlanetScope 3m de paga** + Sentinel-2 + VIIRS + CMEMS) y validación acústica. | Completo |
| **`06_operaciones_y_protocolos_marinos.md`** | Maniobras LARS, protocolos *Failsafe* (*Limp-Home* 25 MN) y límites Beaufort. | Completo |
| **`07_guia_llenado_y_estrategia_cliente.md`** | Estrategia comercial, estructura financiera en 3 Bolsas y presupuesto global. | Completo |
| **`08_preguntas_respuestas_y_fuentes.md`** | Síntesis estructurada de las 37 preguntas de investigación e ingeniería naval/acústica. | Completo |
| **`09_lista_descarte_sensores_y_electronica.md`** | Justificación técnica y financiera de por qué se descartaron paneles solares, motores 12V/24V, brújulas magnéticas y USVs chinos. | Completo |
| **`10_entregable_ejecutivo_clientes_y_bom.md`** | **Entregable Comercial para Socios:** Propuesta en 3 Bolsas, Pitch 6 Slides, ROI, 4 Opciones de Casco (incluyendo Pontón de \$45k MXN + 5 modificaciones) y BOM USA con links. | **Listo para presentar** |
| **`11_arquitectura_web_gis_y_plan_programacion.md`** | **Plan de Programación (Hito Día 21):** Esquema PostGIS, fórmulas HSI Doble Turno, activación Trial PlanetScope 3m y estructura de código FastAPI + n8n + React PWA. | **Listo para codificar** |

---

## Log de Decisiones Clave Congeladas (Inamovibles)

1. **Dos Opciones de Casco Propio vs. 2 Comerciales (Comparativa de 4 Plataformas):**
   - **Opción 1 (Trimarán desde Cero — \$5,600 USD):** Quilla central en Aluminio Naval 5083 CNC + 2 flotadores exteriores PAD Tubomex inyectados con espuma + tanque 60L XLPE con cuello de ganso anti-explosión + cubierta plana "Stealth" (*0 paneles solares*).
   - **Opción 2 (Pontón Recreativo Modificado a Trimarán — \$45,000 MXN base + \$43,500 MXN en 5 modificaciones = \$88,500 MXN / \$4,425 USD):** Aprovecha su **tanque de combustible marino integrado de fábrica (90–150 L)** y añade un 3er pontón central de aluminio 5083 para instrumentos/baterías, disipador de olas (*Wave Deflector*) a $45^\circ$, adecuación de tanque con extractor ISO 8846, soportes con toberas corta-cabos para Pods de 3kW y cubierta ciega "Stealth".
2. **Tren Motriz Industrial de 48V (6.0 kW Totales) + Doble Batería "Anti-Deriva" (10.24 kWh):**
   - **2x Propulsores Brushless Inrunner 48V 3.0 kW (Flipsky 65161)** + **Dual FSESC75200 Pro enfriado por agua** (\$2,800 USD con herrajes y toberas).
   - **Banco Masivo LiFePO4 48V 200Ah (10.24 kWh, ~85 kg)** comprado en México (\$2,650 USD): garantiza **25 millas náuticas de regreso autónomo eléctrico (*Limp-Home*)** si falla el generador a gasolina a 20 millas de la costa.
3. **Geoposicionamiento Dual RTK (2x u-blox ZED-F9P Cobrados al Proyecto):**
   - Se utilizan los **2 receptores F9P** del inventario del consultor y **se cobran en la Bolsa 1 a \$780 USD** con la ventaja de entrega inmediata en Día 1. Proveen *Moving Baseline GPS Yaw* ($0.1^\circ$ de rumbo verdadero inmune al magnetismo de los cables de 125A).
4. **Aviónica, Visión Térmica, Cajas IP68 y Cableado Marino Completo:**
   - **CubePilot Cube Orange+** (\$420 USD) + **NVIDIA Jetson Orin Nano 8GB + 1TB NVMe** (\$609 USD) + **Cámara Térmica FLIR Boson 320** (\$2,450 USD) + **Radar Marino 24 GHz Ainstein** (\$1,100 USD) + **Starlink Mini** (\$599 USD) + **AIS Clase B Em-Trak B921** (\$650 USD) + **RFD900x 915 MHz** (\$250 USD) + **Penetradores WetLink IP68, Cajas de Aluminio IP68 y Cable Estañado UL1426 AWG 2/0** (\$1,300 USD).
5. **Plataforma Satelital de Paga de Máxima Precisión (PlanetScope 3m Diario):**
   - Suscripción comercial **PlanetScope a 3.0 metros diarios** (\$600 USD/mes = **\$3,600 USD por 6 meses de zafra**), combinada con trial de evaluación en Semana 1–2 para demostrar con datos reales desde el principio, fusionada vía **n8n + PostGIS** con Sentinel-2, VIIRS y CMEMS.
6. **Sensores Submarinos Multi-Especie para Renta en Doble Turno (\$7,700 USD):**
   - **Sonar CHIRP 1 kW Garmin GSD 25 + Airmar B265LH (50/200 kHz)** (\$2,600 USD) + **Hidrófono Digital Aquarian H3d-Ethernet** (\$1,900 USD) + **Sonda Turner Cyclops-7F de Clorofila-a / Turbidez / CTD** (\$3,200 USD) para prospectar camarón de noche y rentar coordenadas de sardina/curvina de día.
7. **Flujo Financiero en 3 Bolsas (Inversión Total \$48,679 USD con Trimarán desde Cero o \$47,504 USD con Pontón Modificado):**
   - **Bolsa 1 (EE. UU. — \$22,429 USD):** Pagada directo con tarjeta americana del socio y enviada a su casa en EE. UU. (ahorrando \$5,720 USD de aduana).
   - **Bolsa 2 (México — \$9,850 USD o \$8,675 USD):** Pagada directo en México al astillero y proveedor de baterías LiFePO4.
   - **Bolsa 3 (Honorarios del Consultor — \$16,400 USD):** Pagada en 4 Hitos libres de compra de materiales (Día 21: \$4,800 USD; Semana 4: \$2,800 USD; Semana 6: \$5,600 USD; Semana 8: \$3,200 USD).
