"""
Funciones de análisis estadístico – AquaLimpia S. A.
"""
import pandas as pd
from scipy import stats


def correlaciones(df, objetivo, variables):
    """Correlación de Pearson de cada variable con la variable objetivo, con su p-valor."""
    filas = []
    for var in variables:
        r, p = stats.pearsonr(df[var], df[objetivo])
        filas.append({'variable': var, 'r': round(r, 3), 'r2': round(r ** 2, 3), 'p_valor': p})
    tabla = pd.DataFrame(filas)
    return tabla.sort_values('r', key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


def intervalo_confianza(serie, nivel=0.95):
    """Intervalo de confianza de la media usando la distribución t."""
    return stats.t.interval(nivel, df=len(serie) - 1, loc=serie.mean(), scale=stats.sem(serie))


def resumen_por_planta(df, nivel=0.95):
    """Indicadores promedio por planta e intervalo de confianza de la eficiencia."""
    resumen = df.groupby('planta').agg(
        registros=('planta', 'count'),
        DBO_entrada_prom=('DBO_entrada_mg_L', 'mean'),
        DBO_salida_prom=('DBO_salida_mg_L', 'mean'),
        eficiencia_prom=('eficiencia_remocion_pct', 'mean'),
        tasa_cumplimiento_pct=('cumplimiento_norma', 'mean')
    )
    resumen['tasa_cumplimiento_pct'] = resumen['tasa_cumplimiento_pct'] * 100
    ic = df.groupby('planta')['eficiencia_remocion_pct'].apply(lambda s: intervalo_confianza(s, nivel))
    resumen['eficiencia_ic_inf'] = ic.str[0]
    resumen['eficiencia_ic_sup'] = ic.str[1]
    return resumen.round(2)


def prueba_chi2(df, grupo, resultado):
    """Prueba chi-cuadrado de independencia entre dos variables categóricas."""
    tabla = pd.crosstab(df[grupo], df[resultado])
    chi2, p, gl, _ = stats.chi2_contingency(tabla)
    return {'tabla': tabla, 'chi2': chi2, 'p_valor': p, 'gl': gl}
