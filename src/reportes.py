"""
Funciones de exportación de resultados – AquaLimpia S. A.
"""
import os
import joblib

COLS_OPERACIONES = ['fecha_registro', 'planta', 'caudal_entrada_m3_d', 'DBO_entrada_mg_L',
                    'DBO_salida_mg_L', 'eficiencia_remocion_pct', 'energia_aeracion_kWh',
                    'lodos_generados_kg_d', 'alerta_carga_alta', 'alerta_eficiencia_baja']


def exportar_reportes(df, carpeta='outputs'):
    """Genera los reportes Excel para Operaciones y Gestión Ambiental."""
    os.makedirs(carpeta, exist_ok=True)
    operaciones = df[COLS_OPERACIONES].sort_values(['fecha_registro', 'planta'])
    ambiental = df[['fecha_registro', 'planta', 'DBO_salida_mg_L']].copy()
    ambiental['estado_cumplimiento'] = df['cumplimiento_norma'].map({0: 'No cumple', 1: 'Cumple'})
    ambiental = ambiental.sort_values(['fecha_registro', 'planta'])
    ruta_op = os.path.join(carpeta, 'reporte_operaciones.xlsx')
    ruta_amb = os.path.join(carpeta, 'reporte_gestion_ambiental.xlsx')
    operaciones.to_excel(ruta_op, index=False)
    ambiental.to_excel(ruta_amb, index=False)
    return ruta_op, ruta_amb


def guardar_resultados(resultados, ruta='outputs/resultados_analisis.joblib'):
    """Guarda los resultados del análisis para reutilizarlos sin recalcular."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    joblib.dump(resultados, ruta)
    return ruta


def cargar_resultados(ruta='outputs/resultados_analisis.joblib'):
    """Carga resultados guardados previamente."""
    return joblib.load(ruta)
