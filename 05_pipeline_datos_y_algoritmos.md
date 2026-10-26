# 05. Pipeline de Datos, Modelos Satelitales y Algoritmos

## Metadata de Control
* **Módulo:** SUB-01 (Datos Satelitales) y SUB-05 (Fusión y Predicción).
* **Propósito:** Definir el flujo algorítmico completo desde la ingesta satelital nocturna, generación de polígonos, filtrado in situ del USV hasta la emisión del vector de pesca al capitán.

---

## 1. Diagrama de Flujo del Pipeline Analítico

```
[22:00 hrs] Ingesta Satelital (SST, Clorofila-a, Corrientes)
     │
     ▼
[22:30 hrs] Filtrado Espacial por Batimetría (5 a 30 brazas) y Mascarado de Costas
     │
     ▼
[23:00 hrs] Generación de "Zonas Calientes" (Clustering / Detección de Frentes Térmicos)
     │
     ▼
[00:00 - 05:00 hrs] Enrutamiento Autónomo de USV hacia Polígonos Prioritarios
     │
     ▼
[In Situ] Algoritmo de Validación Robótica (Acústica + Turbidez + Temperatura Fondo)
     │
     ├─► ¿Confirma biomasa? ──► SÍ: Eleva peso estadístico del polígono
     └─► Falso positivo    ──► NO: Descarte inmediato y recalcula ruta a zona 2
     │
     ▼
[05:30 hrs] Fusión Bayesiana / Heurística y Generación del Vector Final
     │
     ▼
[< 06:00 hrs] Despacho de Coordenadas al Capitán del Barco Nodriza y Flota
```

---

## 2. Ingesta Satelital Oceanográfica y Pipeline en Python (GEE + CMEMS)

### Fuentes de Datos y Resolución Superior

| Fuente / Satélite | Parámetro Oceanográfico | Resolución Espacial | Frecuencia y Automatización |
| :--- | :--- | :--- | :--- |
| **Sentinel-2 (ESA via Google Earth Engine API)** | Bandas ópticas B2, B3, B4, B8 (Reflectancia espectral) | **10 m a 20 m por píxel** | Detección de frentes estuarinos y plumas de sedimentos ("chocolatito") saliendo de bocas de esteros tras mareas vaciantes. |
| **Copernicus Marine Service (CMEMS via `copernicusmarine` Python)** | Temperatura de fondo, salinidad de fondo, corrientes superficiales y de fondo, oxígeno disuelto | Cuadrícula oceanográfica costera (~1 km a 4 km) | **Descarga automatizada diaria a las 05:00 AM (\$0 USD)** mediante script en servidor cloud sin intervención humana. |
| **GEBCO / Batimetría Digital** | Profundidad del lecho marino | Matriz batimétrica | **Filtro estricto de 2 a 15 brazas (somero pangas)** y 15 a 30 brazas (faena barco nodriza). |

### Descarte de Falsos Positivos Satelitales
1. **Oxígeno Disuelto en el Fondo:** Si la concentración de $O_2$ cae por debajo de $2\text{ mg/L}$ (zona hipóxica por descomposición algal), el polígono se invalida inmediatamente aunque la superficie muestre alta clorofila.
2. **Termoclina Profunda:** En aguas $>15\text{ m}$, la temperatura superficial satelital (SST) se desacopla del fondo; el algoritmo aplica la temperatura de lecho del modelo hidrodinámico CMEMS.

---

## 3. Algoritmo de Validación In Situ en el USV

El objetivo es eliminar falsos positivos generados por satélite (ej. floraciones algales no aptas, frentes térmicos estériles, basura marina):

$$P_{\text{final}} = w_1 \cdot P_{\text{satélite}} + w_2 \cdot S_{\text{acústico}} + w_3 \cdot S_{\text{fisicoquímico}}$$

* **$S_{\text{acústico}}$ (Firma de Fondo y Ecograma Simrad EK80):**
  * Detección de eco secundario para clasificar dureza del sustrato (el camarón requiere fango arcilloso/limo; fondos de roca o arena gruesa reducen la probabilidad).
  * Densidad de reflectancia acústica justo sobre el lecho marino ($0\text{ a }1.5\text{ m}$ del fondo) en frecuencias de 200/333 kHz durante la noche (desenterramiento biológico).
* **Filtro Hidrofónico de Exclusión:** Si el hidrófono registra chasquidos de alta frecuencia ($>180\text{ dB}$ típicos de *snapping shrimp*), descarta la zona por fondo rocoso.
* **$S_{\text{fisicoquímico}}$ (Perfilador CTD In Situ):**
  * Turbidez de fondo superior al promedio (actividad de remoción bentónica).
  * Temperatura de fondo dentro del rango metabólico óptimo de la especie ($24^\circ\text{C} - 28^\circ\text{C}$).

---

## 4. Despacho y Entrega Operativa (< 06:00 hrs)

El sistema genera automáticamente:
1. **Capas Cartográficas Livianas (`.mbtiles` / `.kml`):** Enviadas por Starlink al barco nodriza para abrir directamente en apps de navegación de cabina (**Navionics, TimeZero, QField**).
2. **Polígono de Mayor Probabilidad:** Polígono delimitado por 4 coordenadas GPS con semáforo Verde/Amarillo.
3. **Rumbo de Aproximación Óptimo:** Vector de navegación para que las pangas tiren sus redes a favor o través de corriente.

---

## 4. Despacho y Entrega Operativa (< 06:00 hrs)

El sistema genera automáticamente:
1. **Polígono de Mayor Probabilidad:** Polígono delimitado por 4 coordenadas GPS.
2. **Rumbo de Aproximación Óptimo:** Vector de navegación para que la flota tire sus redes a favor o través de corriente.
3. **Ficha Resumen para Tripulación:** Métricas visuales simples (Código Semáforo: Verde/Amarillo/Rojo, profundidad sugerida de plomo de red en brazas).
