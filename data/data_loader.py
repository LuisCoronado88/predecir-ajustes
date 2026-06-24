import pandas as pd
import numpy as np
import os

def load_and_clean_data():
    """
    Carga de forma robusta el universo comercial de 659,856 registros reales
    desde la carpeta 'data', aplicando el saneamiento técnico y la ingeniería
    de características sincronizada con el modelo Gradient Boosting.
    """
    # Definimos las rutas exactas donde reside tu dataset real
    posibles_rutas = [
        os.path.join('data', 'DataAjuste_variableajustada.csv'),
        'DataAjuste_variableajustada.csv',
        r'D:\AjusteFacturacion\data\DataAjuste_variableajustada.csv'
    ]
    
    df = None
    ruta_exitosa = None

    # Ciclo de búsqueda y lectura del archivo real
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            for sep in [';', ',']:
                try:
                    # Lectura adaptada al formato de exportación de la base de datos
                    df = pd.read_csv(ruta, encoding='latin1', sep=sep, decimal=',', on_bad_lines='skip')
                    if len(df.columns) > 1:
                        ruta_exitosa = ruta
                        break
                except Exception:
                    continue
            if df is not None:
                break
            
    # Si tras recorrer las rutas no encuentra el CSV, levantamos un error explícito
    if df is None:
        raise FileNotFoundError(
            "❌ CRÍTICO: No se encontró el archivo 'DataAjuste_variableajustada.csv' en la carpeta 'data' ni en las rutas alternas. "
            "Por favor, verifica que el archivo esté copiado correctamente en la ruta del proyecto."
        )

    print(f"📖 Dataset real cargado con éxito desde: {ruta_exitosa}")
    print(f"📊 Total de registros comerciales listos para procesamiento: {len(df):,}")

    # 1. Normalización estricta de las cabeceras de columnas (Minimiza fallos por minúsculas o espacios)
    df.columns = df.columns.str.strip().str.upper()
    
    # 2. Conversión Numérica Avanzada y Saneamiento bajo cero
    columnas_numericas = [
        'FACTURACION_PROMEDIO', 'M3_PROMEDIO', 'VALOR_PAGO_PROMEDIO', 
        'FACTURACION_PERIODO', 'M3_PERIODO', 'AJUSTE_EN_ULT_6_MESES', 'VALOR_AJUSTE_PERIODO'
    ]
    
    for col in columnas_numericas:
        if col in df.columns:
            # Forzar conversión eliminando ruidos latinos de texto o comas erróneas
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            # Neutralización de valores negativos atípicos (Suelo en Cero para auditoría)
            df[col] = df[col].clip(lower=0)
            
    # Forzar consistencia binaria entera en las variables lógicas y objetivo
    for col_binaria in ['AJUSTE_EN_ULT_6_MESES', 'VALOR_AJUSTE_PERIODO']:
        if col_binaria in df.columns:
            df[col_binaria] = df[col_binaria].astype(int)

    # 3. 🔥 INGENIERÍA DE CARACTERÍSTICAS (FEATURE ENGINEERING) REAL
    if 'M3_PERIODO' in df.columns and 'M3_PROMEDIO' in df.columns:
        df['DESVIACION_M3'] = df['M3_PERIODO'] - df['M3_PROMEDIO']
        df['ALERTA_ALTO_CONSUMO'] = np.where(df['M3_PERIODO'] > (df['M3_PROMEDIO'] * 1.5), 1, 0)
        
    if 'FACTURACION_PERIODO' in df.columns and 'FACTURACION_PROMEDIO' in df.columns:
        df['DESVIACION_FACTURACION'] = df['FACTURACION_PERIODO'] - df['FACTURACION_PROMEDIO']

    return df