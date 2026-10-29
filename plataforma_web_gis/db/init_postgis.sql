-- ============================================================================
-- ESQUEMA ESPACIAL POSTGIS TRI-ESPECIE (CAMARÓN, PESCADO Y JAIBA)
-- PLATAFORMA SATELITAL 3M (PLANETSCOPE) + USV TRIMARÁN 48V + STARLINK MINI
-- Sede Operativa: Topolobampo - Ohuira - Santa María (SIN) y Bahía de Kino (SON)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Cooperativas y Clientes (Control de Acceso por Token, Especie y Modalidad)
CREATE TABLE IF NOT EXISTS cooperativas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(120) NOT NULL,
    zona_operacion VARCHAR(80) NOT NULL, -- 'Topolobampo-Ohuira', 'Bahia de Kino'
    especie_contratada VARCHAR(50) NOT NULL DEFAULT 'TRI_ESPECIE', -- 'CAMARON', 'PESCADO', 'JAIBA', 'TRI_ESPECIE'
    tier_contratado VARCHAR(30) NOT NULL DEFAULT 'MVP_BAJO_COSTO', -- 'ETAPA_1_SATELITAL', 'MVP_BAJO_COSTO', 'GRADO_CIENTIFICO'
    access_token VARCHAR(64) UNIQUE NOT NULL,
    suscripcion_activa BOOLEAN DEFAULT TRUE,
    fecha_vencimiento TIMESTAMP WITH TIME ZONE NOT NULL,
    telefono_alerta_whatsapp VARCHAR(30),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Boletines Satelitales Diarios (21:30 PM Camarón / 04:00 AM Jaiba / 04:45 AM Pescado)
CREATE TABLE IF NOT EXISTS boletines_satelitales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fecha_operacion DATE NOT NULL,
    zona_operacion VARCHAR(80) NOT NULL,
    turno VARCHAR(30) NOT NULL, -- 'NOCTURNO_CAMARON' | 'DIURNO_SARDINA' | 'PROSPECCION_JAIBA'
    sensor_tier VARCHAR(30) NOT NULL DEFAULT 'MVP_BAJO_COSTO',
    fuente_optica VARCHAR(80) NOT NULL DEFAULT 'PlanetScope_3m_Daily_8Band + Sentinel2 + CMEMS',
    porcentaje_nubes NUMERIC(5,2) DEFAULT 4.5,
    fase_lunar VARCHAR(40),
    velocidad_marea_nudos NUMERIC(4,2),
    kml_url TEXT,
    gpx_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Polígonos de Alta Probabilidad (Camarón, Pescado y Corredores de Trampas Jaiberas)
CREATE TABLE IF NOT EXISTS poligonos_pesca (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    boletin_id UUID REFERENCES boletines_satelitales(id) ON DELETE CASCADE,
    codigo_zona VARCHAR(30) NOT NULL,
    nombre_canal VARCHAR(100) NOT NULL,
    especie_objetivo VARCHAR(60) NOT NULL, -- 'Camarón Azul/Café', 'Sardina/Curvina/Pargo', 'Jaiba Café/Azul (C. bellicosus/arcuatus)'
    prioridad INT NOT NULL, -- 1 (Rojo/Verde >85%), 2 (Ámbar 70-84%), 3 (Exclusión Roca o Hipoxia)
    score_hsi NUMERIC(5,2) NOT NULL,
    sst_centigrados NUMERIC(4,2),
    temp_fondo_centigrados NUMERIC(4,2),
    salinidad_psu NUMERIC(4,2),
    oxigeno_disuelto_mg_l NUMERIC(4,2) DEFAULT 5.4, -- Crítico para Jaiba (Bloqueo si < 2.2 mg/L)
    sustrato_sidescan VARCHAR(50) DEFAULT 'ECOTONO_ARENA_CONCHAL', -- Side-Scan 800kHz / Oculus 1.2MHz
    densidad_trampas_sugerida_ha INT DEFAULT 0, -- Trampas/nasas por hectárea sugeridas para Jaiba
    alerta_hipoxia_trampas BOOLEAN DEFAULT FALSE,
    turbidez_ndti NUMERIC(5,3),
    clorofila_mg_m3 NUMERIC(6,3),
    profundidad_brazas_min NUMERIC(4,1),
    profundidad_brazas_max NUMERIC(4,1),
    confirmado_por_usv BOOLEAN DEFAULT FALSE,
    riesgo_roca_hidrofono BOOLEAN DEFAULT FALSE,
    recomendacion_tactica TEXT,
    geom GEOMETRY(Polygon, 4326) NOT NULL,
    centroide GEOMETRY(Point, 4326) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_poligonos_geom ON poligonos_pesca USING GIST (geom);

-- 4. Telemetría en Tiempo Real del USV Trimarán Híbrido 48V "Stealth" (Starlink Mini Indispensable)
CREATE TABLE IF NOT EXISTS telemetria_usv (
    id BIGSERIAL PRIMARY KEY,
    timestamp_utc TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usv_id VARCHAR(40) DEFAULT 'TRIMARAN-STEALTH-01',
    sensor_tier VARCHAR(30) DEFAULT 'MVP_BAJO_COSTO', -- 'MVP_BAJO_COSTO' ($53,949) | 'GRADO_CIENTIFICO' ($148,400)
    modo_propulsion VARCHAR(30), -- 'ELECTRICO_STEALTH_3KT', 'HIBRIDO_TRANSITO_11KT', 'LIMP_HOME_25NM'
    voltaje_bus_48v NUMERIC(5,2), -- Nominal 51.2V LiFePO4 (10.24 kWh)
    soc_bateria_pct NUMERIC(5,2),
    autonomia_limp_home_mn NUMERIC(5,1),
    generador_4t_encendido BOOLEAN DEFAULT FALSE,
    starlink_mini_activo BOOLEAN DEFAULT TRUE, -- Indispensable para transmisión mar adentro
    rumbo_rtk_dual_f9p_deg NUMERIC(5,2), -- Moving Baseline 0.1 deg precision
    velocidad_nudos NUMERIC(4,2),
    frecuencia_sonar_khz INT, -- 200 (Camarón) | 50 (Pescado) | 800/1200 (Side-Scan/Oculus Jaiba)
    eco_biomasa_db NUMERIC(5,2),
    ruido_hidrofono_khz NUMERIC(5,2),
    tipo_fondo_acustico VARCHAR(50), -- 'LODO_ORGANICO_OPTIMO', 'ECOTONO_ARENA_CONCHAL', 'ROCA_ALERTA_CHINCHORRO'
    clorofila_turner_ug_l NUMERIC(6,2),
    oxigeno_disuelto_do_mg_l NUMERIC(4,2) DEFAULT 5.4,
    temp_ctd_fondo_c NUMERIC(4,2),
    salinidad_ctd_psu NUMERIC(4,2),
    geom GEOMETRY(Point, 4326) NOT NULL
);

-- 5. Bitácora de Capturas Reportadas por Capitanes (Retroalimentación IA Tri-Especie)
CREATE TABLE IF NOT EXISTS capturas_reportadas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cooperativa_id UUID REFERENCES cooperativas(id),
    poligono_id UUID REFERENCES poligonos_pesca(id),
    embarcacion VARCHAR(80),
    especie VARCHAR(50), -- 'Camarón', 'Pescado/Sardina/Curvina', 'Jaiba Café/Azul'
    kilos_capturados NUMERIC(7,2) NOT NULL,
    lances_o_trampas INT DEFAULT 1,
    consumo_gasolina_litros NUMERIC(6,1),
    comentario_capitan TEXT,
    geom_lance GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- DATOS SEMILLA INICIALES PARA DEMOSTRACIÓN A SOCIOS Y COOPERATIVAS
-- ============================================================================

INSERT INTO cooperativas (nombre, zona_operacion, especie_contratada, tier_contratado, access_token, suscripcion_activa, fecha_vencimiento, telefono_alerta_whatsapp)
VALUES
    ('Alianza Cooperativa Topolobampo - Ohuira', 'Topolobampo-Ohuira', 'TRI_ESPECIE', 'MVP_BAJO_COSTO', 'TOPO-2026-VIP-TOKEN', TRUE, NOW() + INTERVAL '180 days', '+526681000001'),
    ('Flota Sardinera y Escamera del Pacífico', 'Topolobampo-Ohuira', 'PESCADO', 'MVP_BAJO_COSTO', 'SARDINA-2026-DAY-TOKEN', TRUE, NOW() + INTERVAL '180 days', '+526681000002'),
    ('Sociedad Cooperativa Bahía de Kino (Camarón + Jaiba + Escama)', 'Bahia de Kino', 'TRI_ESPECIE', 'GRADO_CIENTIFICO', 'KINO-2026-VIP-TOKEN', TRUE, NOW() + INTERVAL '180 days', '+526621000003')
ON CONFLICT (access_token) DO NOTHING;
