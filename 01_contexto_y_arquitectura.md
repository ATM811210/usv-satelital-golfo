# 01. Contexto y Arquitectura del Proyecto

## Metadata y Directrices del Sistema
* **Dominio:** Pesca industrial de camarón, analítica predictiva marina, robótica marina (USV/UVS).
* **Perfil Interlocutor:** Ingeniero en Cibernética y Electrónica. Nivel técnico alto/especializado (sistemas embebidos, acústica submarina, comunicaciones marinas, sensórica oceanográfica).
* **Propósito del Documento:** Fuente base de contexto para NotebookLM. Máxima densidad informativa, sin relleno sintáctico.

---

## 1. Contexto Operativo y Geográfico
* **Objetivo:** Erradicar la prospección empírica ("a ciegas") mediante predicción satelital y validación robótica in situ en tiempo real.
* **Zona Operativa:** Litoral del Golfo de California (franja costera **Topolobampo, Sinaloa** a **Bahía de Kino, Sonora**).
* **Contexto de Negocio:**
  * Alianza de múltiples cooperativas pesqueras para escalamiento comercial de alto volumen.
  * Antecedente crítico: temporada previa con acopio severamente bajo; eficiencia operativa urgente para viabilidad financiera.

---

## 2. Infraestructura y Capacidad
* **Flota Existente:** >30 pangas (embarcaciones menores de faena artesanal/industrial).
* **Infraestructura Terrestre:** Planta de empaque propia con cadena de procesamiento integral (pelado, descabezado, eviscerado/desvenado), empaque final y logística para exportación.
* **Proyección (Próximo Año):** Integración de un **Barco Nodriza** (embarcación mayor) para remolcar/asistir 20–50 pangas, proveer almacenamiento en frío y actuar como centro de mando y logística en alta mar.

---

## 3. Arquitectura de Solución (Pipeline Diario 24h)

```
[22:00] Ingesta Satelital -> [Madrugada] Prospección USV -> [<06:00] Vector a Nodriza/Flota
```

### Fase 1: Análisis Satelital (22:00 hrs)
* Ingesta y procesamiento de telemetría oceanográfica (SST / Temperatura Superficial, Clorofila-a, turbidez, corrientes).
* Generación de polígonos candidatos ("Zonas Calientes") por probabilidad de biomasa de camarón.

### Fase 2: Validación In Situ en Tiempo Real (Madrugada)
* Despliegue de Vehículos Marítimos de Superficie No Tripulados (**USV / UVS**).
* Misión: Navegación autónoma hacia polígonos satelitales prioritarios para discriminación de biomasa mediante sensórica acústica/óptica local y descarte de falsos positivos.

### Fase 3: Direccionamiento Operativo (< 06:00 hrs)
* Fusión de datos (satélite + telemetría USV).
* Transmisión directa de coordenadas y vectores óptimos al Capitán del Barco Nodriza antes de las 06:00 AM para inicio directo de operaciones de la flota.

---

## 4. Restricciones Técnicas y Justificación de Diseño
* **Inviabilidad de Instrumentación Acústica en Barco Nodriza:**
  * **Ruido Acústico y Cavitación:** Los motores diésel de gran desplazamiento saturan el rango dinámico de ecosondas e hidrófonos, impidiendo la detección de biomasa somera.
  * **Calado y Navegabilidad:** Una embarcación mayor corre riesgo severo de encallamiento en aguas costeras someras y bahías del Golfo de California.
* **Arquitectura Basada en UVS:**
  * Plataformas ligeras de bajo calado para prospección costera segura.
  * Firma acústica nula/mínima (propulsión eléctrica a baterías durante muestreo).
  * Cero riesgo para tripulación humana en exploración nocturna.
