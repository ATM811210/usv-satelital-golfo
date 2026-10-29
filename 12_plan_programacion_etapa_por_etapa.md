# 12. Plan de Acción y Programación Etapa por Etapa (Con Recálculo de Horas Necesarias vs. Avanzadas)

Este documento define la hoja de ruta de ingeniería de software y mecatrónica dividida en **6 Etapas Modulares**, incluyendo el **balance real de horas de ingeniería (Presupuestadas vs. Ya Avanzadas vs. Restantes)** tras haber completado y probado la arquitectura Tri-Especie (**Camarón, Pescado y Jaiba**) y las **3 Modalidades (`ETAPA_1_SATELITAL`, `MVP_BAJO_COSTO` y `GRADO_CIENTIFICO`)**.

---

## 1. Balance Recalculado de Horas de Ingeniería (MVP Web + Cerebro Edge USV)

| Etapa del Plan de Acción | Alcance Técnico Actualizado (Camarón + Pescado + Jaiba) | Horas Totales Necesarias | Horas Ya Avanzadas (Completadas) | Horas Restantes | % Avance | Entregables Listos vs. Tareas Pendientes |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **ETAPA 1:** Conectores Satelitales 3m y Dinámica de Mareas | `PlanetScope3mConnector` (3m 8-bandas), `CMEMS/GEE` (Temp fondo, Salinidad, $DO$, SST) y `tide_and_moon.py`. | **28 hrs** | **20 hrs** | **8 hrs** | **71%** | **Listo:** Estructura API, datasets Topolobampo/Kino y cálculo lunar/marea.<br/>**Falta (8h):** Insertar `PLANET_API_KEY` viva y credenciales `copernicusmarine` en `.env`. |
| **ETAPA 2:** Motor Geofísico Tri-Especie + Base PostGIS | Algoritmos `score_shrimp_night_hsi` (Camarón), `score_sardine_day_hsi` (Pescado) y `score_crab_jaiba_hsi` (Jaiba con filtro $DO$ e hipoxia) + `init_postgis.sql` + Tests. | **36 hrs** | **30 hrs** | **6 hrs** | **83%** | **Listo:** Motor matemático 3 especies, perfiles de sensores y suite `pytest`.<br/>**Falta (6h):** Levantar contenedor `postgis` en VPS Cloud y migrar esquema SQL. |
| **ETAPA 3:** Backend FastAPI + Exportadores `.GPX`/`.KML` + `n8n` | Endpoints REST (`main.py`), bloqueo por Token, selector de 3 niveles de proyecto, exportadores `.GPX`/`.KML` y workflow `n8n`. | **32 hrs** | **24 hrs** | **8 hrs** | **75%** | **Listo:** API FastAPI v2.1, generación `.GPX`/`.KML` y JSON de `n8n`.<br/>**Falta (8h):** Conectar webhook de WhatsApp/Telegram para envío automático (21:30 / 04:00 / 04:45). |
| **ETAPA 4:** App Móvil Capitán (PWA Offline-First) y Portal GIS | Interfaz interactiva `index.html`, Service Worker `sw.js`, Manifest, 3 opciones en vivo (`Camarón`, `Pescado`, `Jaiba`), tablas auditadas y modo Capitán. | **34 hrs** | **30 hrs** | **4 hrs** | **88%** | **Listo:** Portal Web GIS en vivo en GitHub Pages + PWA Offline + Simulador.<br/>**Falta (4h):** Pruebas de campo en celular Android/iOS sin señal en muelle. |
| **SUBTOTAL MVP WEB (Etapas 1 a 4 — Hito Día 21)** | **Plataforma Satelital 3m Tri-Especie + App Capitán** | **130 hrs** | **104 hrs** | **26 hrs** | **80.0%** | **Solo restan 26 horas (~3.5 días de enfoque) para cerrar al 100% la Etapa 1 en servidor productivo.** |
| **ETAPA 5:** Cerebro Edge AI en USV (Jetson Orin Nano / AGX) | `usv_mission_controller.py` + `edge_vision_fusion.py` (FLIR Boson TTC COLREGs, Side-Scan Jaiba 800kHz/Oculus, Sonda $DO$ e Hidrófono H3d). | **48 hrs** | **22 hrs** *(Lógica + Tests)* | **26 hrs** *(Hardware)* | **46%** | **Listo:** Lógica de control, visión, biomasa y 12 unit tests en CI/CD.<br/>**Falta (26h):** Ingesta física Ethernet/Serial con sensores reales en banco. |
| **ETAPA 6:** Supervivencia 48V, Hibridación y Pruebas de Mar | Máquina de estados *Limp-Home* 25 MN (LiFePO4 10.24 kWh), extractor ISO 8846 (90s), failover **Starlink Mini Indispensable** $\rightarrow$ RFD900x 915 MHz. | **42 hrs** | **16 hrs** *(Software)* | **26 hrs** *(En Agua)* | **38%** | **Listo:** Máquina de estados de potencia 48V y simulador de failsafes.<br/>**Falta (26h):** Integración eléctrica con Cube Orange+ / VESC y pruebas de mar. |
| **TOTAL PROYECTO COMPLETO (Etapas 1 a 6)** | **Sistema Satelital 3m + USV Trimarán Híbrido 48V** | **220 hrs** | **142 hrs** | **78 hrs** | **64.5%** | **142 horas ya ejecutadas y respaldadas en GitHub; restan 26h Web + 52h Hardware.** |

---

## 2. Mapa de Arquitectura de las 6 Etapas (Tri-Especie: Camarón, Pescado y Jaiba)

```mermaid
flowchart TD
    subgraph E1["ETAPA 1 (20/28 hrs Completadas): Conectores Satelitales 3m"]
        S1["PlanetScope API (3.0m Diario 8-Bandas)<br/>Trial Evaluación + Suscripción Semestral"]
        S2["Google Earth Engine + NOAA VIIRS<br/>SST Nocturna + Sentinel-2 10m"]
        S3["Copernicus Marine (CMEMS)<br/>Temp Fondo + Salinidad + Oxígeno Disuelto (DO)"]
        S4["Motor Astronómico y Mareas<br/>Fase Lunar + Corriente de Vaciante (Nudos)"]
    end

    subgraph E2["ETAPA 2 (30/36 hrs Completadas): Motor Geofísico Tri-Especie + PostGIS"]
        M1["Opción 1: Camarón (2-12 bz)<br/>NDTI 3m + Termohalino + Exclusión Roca"]
        M2["Opción 2: Pescado/Escama (10-90 bz)<br/>Clorofila-a RedEdge + Frente SST + Talud"]
        M3["Opción 3: Jaiba Bentónica (0.8-8.5 bz)<br/>Oxígeno Disuelto DO >= 3.2 mg/L + Side-Scan Conchal"]
    end

    subgraph E3["ETAPA 3 (24/32 hrs Completadas): Backend FastAPI + .GPX/.KML + n8n"]
        B1["API Multi-Tenant + Selector de 3 Modalidades<br/>(Etapa 1 $11.1k | MVP $53.9k | Científico $148.4k)"]
        B2["Exportador Dual para Plotters Marinos<br/>.GPX (Waypoints/Líneas de Trampas) y .KML"]
        B3["Orquestador n8n: Cortes 21:30 PM (Camarón),<br/>04:00 AM (Jaiba) y 04:45 AM (Pescado)"]
    end

    subgraph E4["ETAPA 4 (30/34 hrs Completadas — HITO 1): App Capitán PWA Offline"]
        A1["Portal GIS + Service Worker (sw.js)<br/>Operación sin señal celular en altamar"]
        A2["Selector en Vivo: Camarón / Pescado / Jaiba<br/>+ Tablas BOM con Mano de Obra Separada"]
        A3["Alertas Acústicas y de Hipoxia de Fondo<br/>(Prohibición de calar trampas si DO < 2.2 mg/L)"]
    end

    subgraph E5["ETAPA 5 (22/48 hrs Completadas): Cerebro Edge AI en USV"]
        U1["Sonar Nadir (Garmin 50/200 kHz o Simrad EK80)<br/>+ Side-Scan Jaiba (800 kHz o Oculus 1.2 MHz)"]
        U2["Hidrófono Dual H3d / icListen HF<br/>Roca (>2.4kHz), Quelas Jaiba (1.2-3.5kHz), Curvina (450Hz)"]
        U3["Sonda Turner / RBRconcerto³ + Sonda Óptica DO<br/>Clorofila-a + Turbidez + Oxígeno Disuelto Fondo"]
    end

    subgraph E6["ETAPA 6 (16/42 hrs Completadas): Supervivencia 48V y Starlink"]
        F1["Control Híbrido 48V + Extractor ISO 8846 (90s)<br/>Sigilo 100% Eléctrico (2.8 - 3.0 kt)"]
        F2["Seguro Anti-Deriva Limp-Home (25 Millas Náuticas)<br/>Banco LiFePO4 10.24 kWh (48V 200Ah)"]
        F3["Starlink Mini DC Indispensable + Backup RFD900x<br/>+ Evasión Nocturna FLIR Boson / Radar 24GHz"]
    end

    E1 --> E2 --> E3 --> E4
    E3 <--> E5 --> E6
```

---

## 3. Plan de Acción Inmediato para Cerrar las 26 Horas Restantes del MVP Web (Compuertas de 15 Minutos)

1. **Bloque Cloud 1 (6 hrs — Base de Datos Espacial PostGIS):**
   - Actualizar `db/init_postgis.sql` con las columnas de **Jaiba (`oxigeno_disuelto_mg_l`, `sustrato_sidescan`, `densidad_trampas_ha`)** y levantar el contenedor `postgis/postgis:16-3.4`.
2. **Bloque Cloud 2 (8 hrs — Ingesta Satelital Viva en `.env`):**
   - Configurar `PLANET_API_KEY` (cuenta Trial/Producción de PlanetScope 3m) y credenciales de Copernicus Marine (`CMEMS_USER` / `CMEMS_PASS`) para automatizar la descarga raster diaria sobre Topolobampo y Bahía de Kino.
3. **Bloque Cloud 3 (8 hrs — Automatización `n8n` y Despacho WhatsApp/Telegram):**
   - Importar `n8n_workflows/flujo_diario_10pm_y_5am.json` agregando el corte de las **04:00 AM para Jaiba (Líneas de Trampas)** junto con el de **21:30 PM (Camarón)** y **04:45 AM (Pescado)**.
4. **Bloque Campo 4 (4 hrs — Prueba Piloto PWA con Capitanes):**
   - Instalar la PWA desde `https://atm811210.github.io/usv-satelital-golfo/` en teléfonos de prueba, verificar caché offline sin señal y descarga de `.GPX` en plotter Garmin/Simrad.
