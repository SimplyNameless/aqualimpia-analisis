# Análisis de desempeño de plantas de tratamiento – AquaLimpia S. A.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SimplyNameless/aqualimpia-analisis/blob/main/notebooks/analisis_aqualimpia.ipynb)

Proyecto de análisis exploratorio para identificar los factores asociados a los incumplimientos de DBO en el efluente tratado de las plantas de AquaLimpia S. A.

## Contexto

AquaLimpia S. A. trata aguas residuales urbanas e industriales en tres plantas. Durante el último periodo se detectaron incumplimientos en la demanda biológica de oxígeno (DBO) del efluente sin un patrón definido. El área de Operaciones planteó tres posibles causas: variaciones del caudal de entrada, cambios en la carga contaminante y diferencias operativas entre plantas.

## Objetivos

**General:** identificar qué factores se asocian a los incumplimientos de DBO para apoyar la priorización de acciones correctivas y respaldar los reportes de cumplimiento ambiental.

**Específicos:**
- Evaluar la relación entre el caudal de entrada y la DBO del efluente (H1).
- Evaluar la relación entre la carga contaminante de entrada y la DBO del efluente (H2).
- Comparar el desempeño y el cumplimiento normativo entre plantas (H3).
- Generar reportes diferenciados para las áreas de Operaciones y Gestión Ambiental.

## Estructura del repositorio

```
aqualimpia-analisis/
├── data/               # Dataset original (no se modifica)
├── notebooks/          # Notebook del análisis
├── outputs/            # Reportes por área (Excel)
├── dashboard/          # Dashboard exploratorio (PNG)
├── requirements.txt    # Versiones de Python y librerías
└── README.md           # Este documento
```

## Datos

Archivo: `data/dataset_set_A_aguas_residuales.xlsx`. Contiene 200 registros de tres plantas (Centro, Norte y Sur), entre el 01-07-2025 y el 28-10-2025.

| Variable | Descripción | Unidad |
|---|---|---|
| `fecha_registro` | Fecha de la medición | – |
| `planta` | Planta de tratamiento | – |
| `caudal_entrada_m3_d` | Caudal de agua residual recibido | m³/d |
| `DBO_entrada_mg_L` | DBO del afluente | mg/L |
| `SST_entrada_mg_L` | Sólidos suspendidos totales del afluente | mg/L |
| `pH_entrada` | pH del afluente | – |
| `energia_aeracion_kWh` | Energía consumida en aireación | kWh |
| `lodos_generados_kg_d` | Lodos generados | kg/d |
| `DBO_salida_mg_L` | DBO del efluente tratado | mg/L |
| `cumplimiento_norma` | Cumplimiento normativo (1 = cumple, 0 = no cumple) | – |

Variable derivada: `eficiencia_remocion_pct = (DBO_entrada − DBO_salida) / DBO_entrada × 100`.

## Proceso

1. **Entorno:** clonado del repositorio y registro de versiones.
2. **Carga y validación:** revisión de dimensiones, valores faltantes y tipos de datos. La fecha se convierte con formato explícito.
3. **Transformación:** cálculo de la eficiencia de remoción.
4. **Análisis:** correlación de Pearson (H1 y H2), comparación por planta y prueba chi-cuadrado de independencia (H3).
5. **Visualización:** dashboard con un panel por hipótesis.
6. **Exportación:** reportes para Operaciones y Gestión Ambiental.

## Cómo reproducir el análisis

1. Abrir el notebook con el botón **Open in Colab**.
2. Ejecutar **Entorno de ejecución → Ejecutar todas**.

El notebook clona este repositorio y genera los resultados en `outputs/` y `dashboard/`. Para trabajar fuera de Colab, instalar las dependencias con:

```bash
pip install -r requirements.txt
```

## Resultados principales

| Hipótesis | Evidencia | Resultado |
|---|---|---|
| H1: Caudal de entrada | r = 0,10 | No respaldada |
| H2: Carga contaminante | r = 0,76 (r² ≈ 0,58) | Respaldada |
| H3: Diferencias entre plantas | Eficiencias de 86,65 % a 87,51 %; χ²(2) = 2,85, p = 0,240 | No respaldada |

Los incumplimientos se asocian principalmente a la carga contaminante que llega a las plantas. La eficiencia de remoción es estable (promedio 87,09 %, DE 3,10), por lo que la DBO de salida depende en gran medida de la DBO de entrada. Las acciones con mayor potencial apuntan a controlar la carga aguas arriba y a ajustar la operación en días de carga alta, más que a intervenir una planta en particular.

![Dashboard exploratorio](dashboard/dashboard_exploratorio.png)

## Reportes generados

| Archivo | Área | Contenido |
|---|---|---|
| `outputs/reporte_operaciones.xlsx` | Operaciones | Fecha, planta, caudal, DBO de entrada y salida, eficiencia, energía, lodos y alertas |
| `outputs/reporte_gestion_ambiental.xlsx` | Gestión Ambiental | Fecha, planta, DBO de salida y estado de cumplimiento |

**Alertas operativas** (umbrales exploratorios derivados de los datos, no normativos):
- **Carga alta:** DBO de entrada sobre el percentil 75 (333,2 mg/L). El 96 % de los días con alerta no cumplieron la norma, pero la alerta solo captura el 31 % del total de incumplimientos.
- **Eficiencia baja:** eficiencia bajo el percentil 10 (82,92 %).

## Limitaciones

- La correlación indica asociación, no causalidad.
- Las muestras por planta (54 a 75 registros) limitan la capacidad de detectar diferencias pequeñas.
- La variable `cumplimiento_norma` presenta inconsistencias con los valores de DBO de salida. Se mantiene tal como viene en los datos originales.

## Autor

Claudio Navarro Vaccaro – Ingeniería en Informática, IACC.
Asignatura: Ciencia de Datos (CIEDT1301), Semana 8.
