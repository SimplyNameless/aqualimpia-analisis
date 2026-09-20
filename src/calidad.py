"""
Funciones de evaluación de calidad de datos – AquaLimpia S. A.
"""
import numpy as np
import pandas as pd


def resumen_completitud(df):
    """Cantidad y porcentaje de valores faltantes por columna."""
    faltantes = df.isna().sum()
    return pd.DataFrame({'faltantes': faltantes,
                         'porcentaje': (faltantes / len(df) * 100).round(2)})


def revisar_duplicados(df, claves):
    """Duplicados exactos y registros que repiten la combinación de claves."""
    exactos = df.duplicated().sum()
    repetidos = df[df.duplicated(claves, keep=False)].sort_values(claves)
    return {'duplicados_exactos': int(exactos),
            'registros_con_clave_repetida': len(repetidos),
            'combinaciones_repetidas': repetidos.groupby(claves).ngroups,
            'detalle': repetidos}


def revisar_rangos(df, reglas):
    """Cuenta los valores fuera del rango válido definido para cada columna."""
    filas = []
    for col, (minimo, maximo) in reglas.items():
        fuera = ((df[col] < minimo) | (df[col] > maximo)).sum()
        filas.append({'variable': col, 'min_valido': minimo, 'max_valido': maximo,
                      'min_observado': df[col].min(), 'max_observado': df[col].max(),
                      'fuera_de_rango': int(fuera)})
    return pd.DataFrame(filas)


def detectar_atipicos_iqr(df, columnas, factor=1.5):
    """Cuenta valores atípicos por columna según el criterio del rango intercuartílico."""
    filas = []
    for col in columnas:
        q1, q3 = np.percentile(df[col], [25, 75])
        iqr = q3 - q1
        inf, sup = q1 - factor * iqr, q3 + factor * iqr
        atipicos = ((df[col] < inf) | (df[col] > sup)).sum()
        filas.append({'variable': col, 'limite_inf': round(inf, 2),
                      'limite_sup': round(sup, 2), 'atipicos': int(atipicos)})
    return pd.DataFrame(filas)


def revisar_consistencia_cumplimiento(df, col_valor='DBO_salida_mg_L', col_estado='cumplimiento_norma'):
    """Compara la etiqueta de cumplimiento con los valores de DBO de salida."""
    cumple = df.loc[df[col_estado] == 1, col_valor]
    no_cumple = df.loc[df[col_estado] == 0, col_valor]
    umbral_implicito = cumple.max()
    return {'max_valor_cumple': umbral_implicito,
            'min_valor_no_cumple': no_cumple.min(),
            'no_cumple_bajo_umbral': int((no_cumple <= umbral_implicito).sum()),
            'total_no_cumple': len(no_cumple)}


def cobertura_temporal(df, col_fecha='fecha_registro', col_grupo='planta'):
    """Días con al menos un registro por grupo, respecto del total de días del periodo."""
    dias_periodo = (df[col_fecha].max() - df[col_fecha].min()).days + 1
    resumen = df.groupby(col_grupo).agg(registros=(col_fecha, 'count'),
                                        dias_con_registro=(col_fecha, 'nunique'))
    resumen['dias_periodo'] = dias_periodo
    resumen['cobertura_pct'] = (resumen['dias_con_registro'] / dias_periodo * 100).round(1)
    return resumen
