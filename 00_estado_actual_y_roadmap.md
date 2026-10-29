# 00. Estado Actual del Proyecto y Roadmap de Ingeniería (Línea Base Auditada Tri-Especie)

## Resumen Ejecutivo de Una Página (SSOT / Context Primer)
* **Proyecto:** Plataforma Satelital Comercial Diaria (3.0 m) y Vehículo Autónomo de Superficie (USV Trimarán Híbrido 48V "Stealth") para Prospección Pesquera Tri-Especie (**1. Camarón Noche**, **2. Pescado/Escama Día** y **3. Jaiba Bentónica**).
* **Zona Geográfica:** Golfo de California (Sistema Lagunar Topolobampo–Ohuira–Santa María, SIN $\leftrightarrow$ Bahía de Kino / Guaymas, SON).
* **Director de Ingeniería:** Ingeniero en Cibernética y Electrónica.
* **Avance Actual del MVP Web (Etapas 1 a 4 — Hito Día 21):** **90.8% Completado (118 de 130 horas ejecutadas, 100% del código y Docker listos y probados con 14 tests unitarios en verde)**. Solo restan **12 horas operativas** al activar las llaves vivas del cliente.

---

## Índice Maestro de la Documentación Pública en el Repositorio

| Archivo | Propósito Principal | Estado |
| :--- | :--- | :--- |
| **`CONTEXTO_MAESTRO.md`** | Manifiesto maestro unificado de contexto técnico y fundamentos físicos/biológicos. | **Activo (SSOT)** |
| **`00_estado_actual_y_roadmap.md`** | Snapshot ejecutivo, control documental y avance de horas de ingeniería. | **Actualizado** |
| **`01_contexto_y_arquitectura.md`** | Fundamentos de negocio, perfil operativo y restricciones del Golfo de California. | Completo |
| **`02_bitacora_investigacion.md`** | Matriz de subsistemas y Registro de Decisiones de Arquitectura (ADR-001 a ADR-007). | Completo |
| **`03_especificaciones_hardware_usv.md`** | **Línea Base de Hardware:** Propulsión 48V 6kW, Baterías LiFePO4 10.24 kWh, Sensores MVP vs. Científico y Cajas IP68. | **Actualizado** |
| **`04_comunicaciones_y_telemetria.md`** | **Starlink Mini (Indispensable)**, RFD900x (915 MHz 40+ km), Transponder AIS Clase B SEMAR y tramas NMEA/KML. | Completo |
| **`05_pipeline_datos_y_algoritmos.md`** | Fusión satelital diaria (**PlanetScope 3m** + Sentinel-2 + VIIRS + CMEMS) y validación acústica. | Completo |
| **`06_operaciones_y_protocolos_marinos.md`** | Maniobras LARS, protocolos *Failsafe* (*Limp-Home* 25 MN) y límites Beaufort. | Completo |
| **`07_guia_llenado_y_estrategia_cliente.md`** | Estrategia comercial y estructura financiera. | Completo |
| **`09_lista_descarte_sensores_y_electronica.md`** | Matriz comparativa **MVP Comercial vs. Grado Científico** y sensores desbloqueados para Jaiba. | **Actualizado** |
| **`10_entregable_ejecutivo_clientes_y_bom.md`** | **Entregable Comercial Auditado:** Etapa 1 Solo Satélite (\$11,120 USD), MVP Trimarán Completo (\$53,949 USD) y Grado Científico (\$148,400 USD) con Mano de Obra separada. | **Listo para presentar** |
| **`11_arquitectura_web_gis_y_plan_programacion.md`** | Esquema PostGIS, fórmulas HSI y arquitectura FastAPI + n8n + PWA. | Completo |
| **`12_plan_programacion_etapa_por_etapa.md`** | **Plan de Acción Recalculado:** Horas totales, horas ya avanzadas y horas restantes por etapa. | **Actualizado** |
| **`13_guia_usuario_whatsapp_clientes.md`** | **Guía de Navegación de la Página Web (Pestaña por Pestaña) + Manual de Uso del Catamarán/Trimarán USV 48V.** | **Nuevo** |

---

## Resumen de las 3 Modalidades Comerciales Auditadas (Mano de Obra Separada y Starlink Indispensable)

1. **Modalidad 1 — Etapa 1 Independiente (Solo Análisis Satelital 3.0m Tri-Especie + App Día 21, Sin USV): \$11,120 USD**
   - **Datos Satelitales de Máxima Precisión (6 Meses):** PlanetScope 3.0m Diario 8-Bandas (\$3,600 USD polígono $600\text{ km}^2$ o \$7,500 USD cobertura regional extendida) + Cloud PostGIS/n8n (\$720 USD) = **\$4,320 USD** (o \$8,220 USD extendida).
   - **Mano de Obra de Ingeniería y Software Tri-Especie (Separada):** **\$6,800 USD**.
2. **Modalidad 2 — USV Trimarán Híbrido 48V MVP Comercial Completo (Camarón + Pescado + Jaiba): \$53,949 USD (Pontón) / \$55,124 USD (Casco Cero)**
   - **Materiales Navales, Propulsión 48V 6kW, Batería LiFePO4 10.24 kWh, Generador 4T y Aviónica (2x RTK F9P, Jetson, FLIR, Radar, Cajas IP68):** **\$17,429 USD** (con Pontón) / **\$18,604 USD** (Casco Cero).
   - **Enlace Satelital Embarcado INDISPENSABLE:** Antena **Starlink Mini DC (\$599) + 6 Meses Servicio Roam/Marítimo (\$900)** + Backup RFD900x 915 MHz (\$250) = **\$1,749 USD**.
   - **Paquete de Sensores Submarinos Tri-Especie:** Garmin CHIRP 50/200 kHz (\$2,600) + **Side-Scan Jaiba 800 kHz (\$1,850)** + Sonda Turner Clorofila/Turbidez/CTD (\$3,200) + **Sonda Óptica DO Industrial (\$950)** + Hidrófono Aquarian H3d (\$1,900) = **\$10,550 USD**.
   - **Datos Satelitales 3.0m (6 Meses PlanetScope + Cloud):** **\$4,320 USD**.
   - **Mano de Obra Separada:** **\$3,500 USD** (Astillero Naval TIG/Mecánica) + **\$16,400 USD** (Ingeniería de Control, Software Tri-Especie e Integración en 4 Hitos).
3. **Modalidad 3 — USV Trimarán 48V Grado Científico (INAPESCA / CIBNOR / Exportación): \$148,400 USD**
   - Incluye Ecosonda Multifrecuencia **Simrad EK80 WBT Mini** (\$24,500) + **Cámara Acústica Multihaz Oculus M1200d + Side-Scan Edgetech** (\$31,500) + **Perfilador RBRconcerto³ CTD-DO-Chl** (\$13,600) + **Hidrófono Calibrado icListen HF** (\$8,800) + **Starlink Marítimo Prioritario** (\$3,500) + **PlanetScope Regional + Radar SAR** (\$12,600) + Materiales/Aviónica (\$25,400) + Mano de Obra Astillero (\$4,500) + Ingeniería y Calibración Acústica (\$24,000).
