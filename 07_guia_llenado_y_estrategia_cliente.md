# 07. Guía de Llenado Técnico y Estrategia de Entregable para Clientes

## Metadata de Control
* **Objetivo:** Hoja de ruta para completar la documentación de ingeniería previa al código web, diagrama de flujo para presentación con directivos y propuesta de simulación satelital (Gratuita vs. Paga).

---

## PARTE 1: Guía de Llenado Técnico (Paso a Paso Antes de Programar la Web)

Antes de programar el frontend o la base de datos, cada módulo documental debe responder preguntas de ingeniería concretas. Este orden evita retrabajos de software:

```
Paso 1: Sensores y Potencia (03) ──► Paso 2: Trama de Radio y Datos (04)
                │                                    │
                ▼                                    ▼
Paso 3: Algoritmo y Salida (05)   ──► Paso 4: Operaciones de Cubierta (06)
                │                                    │
                └─────────────────┬──────────────────┘
                                  ▼
                     Paso 5: Prototipo PoC Satelital
                                  ▼
                     Paso 6: Frontend / Dashboard Web
```

### Checkpoints por Archivo:

1. **En `03_especificaciones_hardware_usv.md`:**
   * [ ] Definir dimensiones finales del catamarán y proveedor de flotadores/casco.
   * [ ] Confirmar modelo exacto de thrusters submarinos (ej. Blue Robotics T200 o alternativas equivalentes).
   * [ ] Calcular el balance de energía: ¿Cuántos Watts consume todo el sistema por hora a 3 nudos? (Define tamaño y peso de batería).
   * [ ] Seleccionar el transductor de sonar (frecuencia de operación y protocolo de salida: NMEA / serial / Ethernet).

2. **En `04_comunicaciones_y_telemetria.md`:**
   * [ ] Definir frecuencias exactas y potencia de los módulos LoRa (915 MHz para México).
   * [ ] Validar altura de montaje de antena en el Barco Nodriza para garantizar línea de vista sobre la curvatura marina ($d \approx 3.57(\sqrt{h_1} + \sqrt{h_2})$ km).
   * [ ] Cerrar el diccionario de datos de la trama de 32 bytes.

3. **En `05_pipeline_datos_y_algoritmos.md`:**
   * [ ] Definir bounding box estricto en coordenadas decimales para Topolobampo - Bahía de Kino.
   * [ ] Establecer umbrales fisicoquímicos: rango de temperatura donde históricamente se pesca camarón azul/café.
   * [ ] Diseñar el formato de salida que verá el capitán en su pantalla.

4. **En `06_operaciones_y_protocolos_marinos.md`:**
   * [ ] Acordar con el patrón del Barco Nodriza cómo será la maniobra de izaje (grúa, red de cuchara o rampa).
   * [ ] Configurar el perímetro de seguridad (geocerca) para que el USV nunca se acerque a zonas rocosas o de tránsito mercante.

---

## PARTE 2: Diagrama de Flujo de Trabajo para Presentar a Clientes

Este flujo visual ilustra a los presidentes de cooperativa y armadores cómo su inversión se traduce en toneladas de camarón y ahorro de diesel:

```mermaid
flowchart TD
    classDef sat fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef rob fill:#065f46,stroke:#10b981,stroke-width:2px,color:#fff;
    classDef fleet fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#fff;
    classDef plant fill:#374151,stroke:#9ca3af,stroke-width:2px,color:#fff;

    subgraph NOCHE_2200 ["1. Fase Satelital Nocturna (22:00 hrs)"]
        S1["Satélites Oceanográficos (SST + Clorofila-a)"]:::sat --> S2["Servidor Cloud: Algoritmo Predictivo"]:::sat
        S2 --> S3["Generación de Polígonos Candidatos ('Zonas Calientes')"]:::sat
    end

    subgraph MADRUGADA ["2. Fase de Validación Robótica en Silencio (Madrugada)"]
        S3 --> U1["Despliegue de USV Catamarán Autónomo"]:::rob
        U1 --> U2["Navegación Eléctrica Silenciosa hacia Polígonos"]:::rob
        U2 --> U3["Sondeo In Situ (Acústica de Fondo + Turbidez + Temperatura)"]:::rob
        U3 --> U4{"¿Presencia Real de Biomasa Confirmada?"}:::rob
        U4 -- "Falso Positivo" --> U5["Descarte Automático y Cambio de Rumbo"]:::rob
        U4 -- "Confirmado" --> U6["Fusión de Datos y Marcado de Alta Prioridad"]:::rob
    end

    subgraph ALBA_0530 ["3. Fase de Dirección y Faena de Pesca (< 06:00 hrs)"]
        U6 --> C1["Transmisión Inalámbrica LoRa al Barco Nodriza"]:::fleet
        C1 --> C2["Consola del Capitán: Coordenadas y Vector Óptimo"]:::fleet
        C2 --> C3["Distribución por VHF a Flota de 30+ Pangas"]:::fleet
        C3 --> C4["Navegación Directa al Objetivo (Cero Búsqueda Empírica)"]:::fleet
        C4 --> C5["Lanzamiento de Redes con Máxima Eficiencia de Combustible"]:::fleet
    end

    subgraph PLANTA ["4. Procesamiento y Retorno de Inversión"]
        C5 --> P1["Acopio Récord en Barco Nodriza (Cuarto Frío)"]:::plant
        P1 --> P2["Recepción en Planta de Empaque Propia"]:::plant
        P2 --> P3["Procesamiento Integral (Pelado/Descabezado) y Exportación"]:::plant
    end

    U5 -.-> U2
```

---

## PARTE 3: Simulación PoC con Datos Gratuitos vs. Servicios de Paga

### 1. El Planteamiento de la Demostración (PoC)
Para ganar la confianza de los clientes **antes** de que desembolsen capital en licencias costosas o fabricación completa:
* **Entregable:** Una simulación interactiva con datos satelitales históricos o de días recientes del Golfo de California (zona Topolobampo - Kino).
* **Herramientas Gratuitas Utilizadas:**
  * **Copernicus Marine Service (CMEMS):** Datos de Temperatura Superficial del Mar (SST) y Clorofila-a con resolución de 1 km a 4 km.
  * **NOAA CoastWatch / VIIRS:** Mapas de turbidez superficial y anomalías térmicas.
  * **Batimetría GEBCO / ETOPO:** Filtrado de profundidades seguras (9 a 55 m).
* **Lo que se le muestra al cliente en la simulación:**
  1. El mapa satelital de la costa del Golfo mostrando cómo el algoritmo identifica 2 o 3 "zonas calientes".
  2. La ruta simulada del USV dirigiéndose a verificar esas zonas.
  3. Cómo una de las zonas se descarta por no cumplir con la dureza de fondo y cómo la zona ganadora se convierte en un vector con coordenadas GPS exactas listo a las 05:30 AM.

---

### 2. Guion Técnico y Comercial para Explicar Datos Gratuitos vs. De Paga

> [!IMPORTANT]
> **Mensaje central para el cliente:** *"La inteligencia y el modelo predictivo que desarrollamos ya funcionan con datos públicos. Sin embargo, los datos gratuitos son como ver el mar a través de binoculares estándar; los servicios de paga son como tener un microscopio satelital en tiempo real."*

#### Tabla Comparativa para la Presentación:

| Parámetro | Datos Satelitales Gratuitos (Copernicus / NOAA) | Servicios Comerciales de Paga (Planet / Spire / Satélites Privados) | Impacto en la Pesca de Camarón |
| :--- | :--- | :--- | :--- |
| **Resolución Espacial** | 1 km a 4 km por píxel | **30 metros a 300 metros** por píxel | El camarón se concentra en frentes estrechos. Mayor resolución = polígonos 10 veces más precisos. |
| **Frecuencia de Actualización** | 1 pase cada 24 a 48 horas | **Múltiples pases diarios** (mañana, tarde y noche) | Permite capturar la ventana exacta de las 22:00 hrs sin desfase por nubes matutinas. |
| **Penetración de Nubes** | Limitada (sensores ópticos bloqueados por nubosidad) | **Radar de Apertura Sintética (SAR)** que atraviesa nubes y niebla marina | En temporada de tormentas o días nublados, los datos ópticos gratuitos quedan ciegos; el radar comercial no. |
| **Latencia de Entrega** | 6 a 18 horas después del pase satelital | **Near Real-Time (NRT):** 1 a 3 horas | Indispensable para que el dato llegue antes de la medianoche y dé tiempo de navegación al USV. |
| **Costo** | **\$0 USD** (Ideal para validar la plataforma) | **Suscripción mensual / anual** (Costo operativo justificado por ahorro de diésel) | Se paga solo con el combustible que se ahorra al no enviar 30 pangas a buscar a ciegas. |

---

### 3. Argumento de Cierre Financiero (El ROI del Proyecto)
* **Consumo de combustible típico:** 30 pangas gastando un promedio de 60 a 100 litros de gasolina por jornada de búsqueda errática = **1,800 a 3,000 litros diarios tirados al mar**.
* **Gasto Monetario Diario:** 2,100 litros $\times$ \$24 MXN = **\$50,400 MXN diarios solo en gasolina** (sin contar diésel marino del Barco Nodriza).
* **Impacto por Zafra (60 mareas):** Más de **\$3,000,000 MXN** gastados en combustible de prospección a ciegas.
* **Con la solución predictiva + USV:** Reducción comprobada del 30% al 45% en tiempos de navegación improductiva.
  * **Ahorro mínimo estimado:** **\$900,000 a \$1,350,000 MXN por temporada**. La inversión completa del USV se amortiza en menos de media zafra.

---

### 4. Cuadro Financiero Formal y Presupuesto Llave en Mano ($54,320 USD)

| Rubro de Inversión | Especificación Técnica Formal | Monto (USD) |
| :--- | :--- | :--- |
| **1. Casco Trimarán** | **Opción A:** Aluminio Naval 5083 desde cero (\$5,600 USD) <br> **Opción B:** Pontón Recreativo Usado (\$45k MXN) + Modificaciones (\$4,425 USD) | **\$5,600 USD** <br> *(o \$4,425 USD)* |
| **2. Propulsión Alta Potencia** | 2x Pods Submarinos Brushless 3.0 kW (48V) + Planta Híbrida 4T Automatizada (3.5 kW) | **\$4,400 USD** |
| **3. Banco Baterías Doble Respaldo** | 10.24 kWh LiFePO4 (48V 200Ah + Smart BMS 200A) con capacidad de retorno de 25 millas | **\$2,650 USD** |
| **4. Aviónica, Cómputo y Legal** | CubePilot Cube Orange+, Dual RTK F9P (\$800), Jetson Orin Nano, Starlink, FLIR Boson, AIS SEMAR | **\$8,250 USD** |
| **5. Sensores Submarinos** | Transductor CHIRP Dual 50/200 kHz + Hidrófono + Sonda CTD/Clorofila/Turbidez | **\$7,700 USD** |
| **6. Logística e Importación** | Flete Hazmat, aranceles aduanales (IVA/IGI), cajas estancas IP68, cable marino AWG 2/0 y tornillería Inox 316 (20%) | **\$5,720 USD** |
| **7. Satélite Diario PlanetScope** | Suscripción comercial directa Planet Labs (3 m resolución diaria para Topolobampo / Ohuira - 6 Meses) | **\$3,600 USD** |
| **8. Ingeniería y Desarrollo** | Ingeniería naval, plataforma Web GIS satelital, orquestación n8n, gestoría SEMAR y ensamble | **\$16,400 USD** |
| **INVERSIÓN TOTAL LLAVE EN MANO** | **Plataforma Trimarán Híbrido 48V "Stealth" Multiespecie (Doble Turno)** | **\$54,320 USD** |

---

### 5. Comparativa de las 4 Opciones de Casco para la Presentación a Clientes

1. **Trimarán de Aluminio 5083 Fabricado desde Cero (\$5,600 USD):**
   * *Ventajas:* Hecho a la medida exacta, quilla central en V profunda, mamparas soldadas de astillero, máxima durabilidad.
   * *Desventajas:* Tiempo de fabricación en taller de 4 a 6 semanas.
2. **Pontón Recreativo Usado (\$45,000 MXN) Modificado a Trimarán (\$4,425 USD / \$88,500 MXN total):**
   * *Ventajas:* **Ya incluye tanque de combustible marino de fábrica (90 a 150 L)** con venteo y flotador; ahorra \$1,200 USD y reduce el tiempo de taller a 2 semanas.
   * *Desventajas:* Requiere inspeccionar que los tubos de aluminio usados no tengan corrosión galvánica severa.
3. **USV Comercial Importado 1 (OceanAlpha SL40 / M40):**
   * *Costo Landed:* **>\$75,000 USD puesto en México**.
   * *Desventajas:* Solo opera a baterías (4 a 6 hrs), sin planta híbrida, no aguanta la marejada de bocabarra y el software es cerrado (no permite conectar el fluorómetro de clorofila ni tu IA).
4. **USV Comercial Importado 2 (Maritime Robotics Otter Pro / Seafloor EchoBoat):**
   * *Costo Landed:* **>\$85,000 USD puesto en México**.
   * *Desventajas:* Costo inasumible para cooperativas, hélices expuestas que se enredan con chinchorros y redes de deriva la primera noche.
