"""
Funciones de carga y preparación de datos – AquaLimpia S. A.
"""
import numpy as np
import pandas as pd


def cargar_datos(ruta):
    """Carga el dataset y convierte la fecha con formato explícito."""
    df = pd.read_excel(ruta)
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], format='%Y-%m-%d')
    return df


def calcular_eficiencia(df, col_entrada='DBO_entrada_mg_L', col_salida='DBO_salida_mg_L'):
    """Agrega la eficiencia de remoción de DBO (%)."""
    df = df.copy()
    entrada = df[col_entrada].to_numpy(dtype=float)
    salida = df[col_salida].to_numpy(dtype=float)
    df['eficiencia_remocion_pct'] = np.round((entrada - salida) / entrada * 100, 2)
    return df


def marcar_alertas(df, pct_carga=75, pct_eficiencia=10):
    """Agrega alertas de carga alta y eficiencia baja según percentiles."""
    df = df.copy()
    umbral_carga = np.percentile(df['DBO_entrada_mg_L'], pct_carga)
    umbral_eficiencia = np.percentile(df['eficiencia_remocion_pct'], pct_eficiencia)
    df['alerta_carga_alta'] = df['DBO_entrada_mg_L'] > umbral_carga
    df['alerta_eficiencia_baja'] = df['eficiencia_remocion_pct'] < umbral_eficiencia
    umbrales = {'carga_alta_mg_L': umbral_carga, 'eficiencia_baja_pct': umbral_eficiencia}
    return df, umbrales
