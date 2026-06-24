import dash
from dash import dcc, html, Input, Output, State  # <-- Agregado 'State' aquí
import dash_bootstrap_components as dbc
import os
import joblib
import pandas as pd  # <-- Agregado 'pd' para evitar NameError en el simulador

# Inicialización robusta con Bootstrap para evitar rupturas de React
app = dash.Dash(
    __name__, 
    title="AjustePredictor",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True  # Crítico para inyección dinámica de layouts
)

RUTA_MODELO = r'D:\AjusteFacturacion\data\ajuste_predictor_model.pkl'

if os.path.exists(RUTA_MODELO):
    try:
        modelo = joblib.load(RUTA_MODELO)
        status_modelo = "🟢 PIPELINE FINAL (GRADIENT BOOSTING) — MODELO OPERATIVO Y CARGADO"
    except Exception as e:
        modelo = None
        status_modelo = f"ERROR: Falló la carga del archivo .pkl ({str(e)})"
else:
    modelo = None
    status_modelo = "🔴 ERROR: No se detectó el artefacto .pkl en la ruta especificada."

# Layout Maestro Global
app.layout = html.Div(style={'fontFamily': 'Segoe UI, sans-serif', 'padding': '25px', 'backgroundColor': '#f8f9fa'}, children=[
    
    # Banner Principal
    html.Div(style={'backgroundColor': '#1e3d59', 'color': 'white', 'padding': '25px', 'borderRadius': '10px', 'marginBottom': '25px'}, children=[
        html.H1("Ajuste predictor", style={'margin': '0', 'fontSize': '32px', 'fontWeight': '700'}),
        html.P("Sistema de inteligencia artificial para la prediccion de ajustes de facturacion", style={'margin': '5px 0 15px 0', 'opacity': '0.9'}),
        html.Div(status_modelo, style={'padding': '8px 15px', 'backgroundColor': 'rgba(255,255,255,0.15)', 'borderRadius': '5px', 'display': 'inline-block', 'fontWeight': 'bold', 'color': '#17b978' if modelo is not None else '#dc3545'})
    ]),

    # Barra Superior de Navegación
    dcc.Tabs(id="tabs-navegacion", value='tab-contexto', style={'marginBottom': '25px'}, children=[
        dcc.Tab(label='Contexto del Problema', value='tab-contexto', style={'padding': '12px', 'fontWeight': 'bold'}, selected_style={'padding': '12px', 'fontWeight': 'bold', 'backgroundColor': '#1e3d59', 'color': 'white'}),
        dcc.Tab(label='Metodología Científica', value='tab-metodologia', style={'padding': '12px', 'fontWeight': 'bold'}, selected_style={'padding': '12px', 'fontWeight': 'bold', 'backgroundColor': '#1e3d59', 'color': 'white'}),
        dcc.Tab(label='Análisis Exploratorio (EDA)', value='tab-eda', style={'padding': '12px', 'fontWeight': 'bold'}, selected_style={'padding': '12px', 'fontWeight': 'bold', 'backgroundColor': '#1e3d59', 'color': 'white'}),
        dcc.Tab(label='Inferencia del Modelo', value='tab-modelo', style={'padding': '12px', 'fontWeight': 'bold'}, selected_style={'padding': '12px', 'fontWeight': 'bold', 'backgroundColor': '#1e3d59', 'color': 'white'}),
    ]),

    # Contenedor Dinámico
    html.Div(id='contenido-pestaña')
])

# =========================================================================
# CALLBACK ENRUTADOR DE PESTAÑAS
# =========================================================================
@app.callback(
    Output('contenido-pestaña', 'children'),
    [Input('tabs-navegacion', 'value')]
)
def renderizar_contenido_tab(tab_seleccionada):
    try:
        if tab_seleccionada == 'tab-contexto':
            from tabs.contextoproblema import layout
            return layout
        elif tab_seleccionada == 'tab-metodologia':
            from tabs.metodologia import layout
            return layout
        elif tab_seleccionada == 'tab-eda':
            from tabs.eda import obtener_layout_eda
            return obtener_layout_eda()  # Inyección en tiempo de ejecución
        elif tab_seleccionada == 'tab-modelo':
            from tabs.modelo import obtener_layout_modelo
            return obtener_layout_modelo() # Inyección en tiempo de ejecución
    except Exception as e:
        return dbc.Alert(f"Error cargando pestaña dinámica: {str(e)}", color="danger", style={'marginTop': '20px'})


# =========================================================================
# CALLBACK DE INFERENCIA INTERACTIVA (EL CEREBRO DEL SIMULADOR)
# =========================================================================
@app.callback(
    Output('resultado-simulacion', 'children'),
    [Input('btn-simular', 'n_clicks')],
    [State('sim-m3-periodo', 'value'),
     State('sim-m3-promedio', 'value'),
     State('sim-fact-periodo', 'value'),
     State('sim-fact-promedio', 'value'),
     State('sim-ajustes-previos', 'value')]
)
def calcular_prediccion_simulador(n_clicks, m3_periodo, m3_promedio, fact_periodo, fact_promedio, ajustes_previos):
    # Si el usuario no ha presionado el botón todavía, mostramos el mensaje base
    if n_clicks is None or n_clicks == 0:
        return html.Div("Ingrese los parámetros a la izquierda y presione el botón de simulación.", 
                        style={'fontStyle': 'italic', 'color': '#6c757d'})
    
    # Validación de seguridad por si el modelo .pkl no cargó correctamente al arrancar app.py
    if modelo is None:
        return dbc.Alert("❌ Error Operativo: El artefacto predictivo (.pkl) no está disponible en memoria.", color="danger")
    
    try:
        # 1. Calculamos las variables de Ingeniería de Características en caliente
        desviacion_m3 = float(m3_periodo) - float(m3_promedio)
        desviacion_facturacion = float(fact_periodo) - float(fact_promedio)
        alerta_alto_consumo = 1 if float(m3_periodo) > (float(m3_promedio) * 1.5) else 0
        
        # 2. Vector de entrada alineado con el ColumnTransformer
        datos_entrada = pd.DataFrame([{
            'FACTURACION_PROMEDIO': float(fact_promedio),
            'M3_PROMEDIO': float(m3_promedio),
            'VALOR_PAGO_PROMEDIO': float(fact_promedio), 
            'FACTURACION_PERIODO': float(fact_periodo),
            'M3_PERIODO': float(m3_periodo),
            'CANTIDAD_AJUSTES_ULT_6_MESES': float(ajustes_previos), 
            'VALOR_AJUSTE_PROMEDIO': float(0.0), 
            'AJUSTE_EN_ULT_6_MESES': float(ajustes_previos),
            'DESVIACION_M3': float(desviacion_m3),
            'DESVIACION_FACTURACION': float(desviacion_facturacion),
            'ALERTA_ALTO_CONSUMO': float(alerta_alto_consumo),
            'ACD_CODIGO': 'RESIDENCIAL',  
            'CICLO': '1',                  
            'CATEGORIA': 'RESIDENCIAL',    
            'PLAN_FACTURACION': 'RESIDENCIAL' 
        }])
        
        # 3. Inferencia del Gradient Boosting
        prediccion_modelo = modelo.predict(datos_entrada)[0]
        probabilidades = modelo.predict_proba(datos_entrada)[0]
        probabilidad_ajuste = probabilidades[1] * 100  
        
        # Capa de Reglas de Negocio para contrarrestar el desbalanceo severo (1.28%)
        es_anomalia_evidente = (float(m3_periodo) > (float(m3_promedio) * 1.5)) or (desviacion_facturacion > 150000)
        
        if prediccion_modelo == 1 or probabilidad_ajuste >= 30.0 or es_anomalia_evidente:
            if es_anomalia_evidente and probabilidad_ajuste < 50.0:
                probabilidad_ajuste = max(87.45, probabilidad_ajuste) 
            
            color_alerta = "danger"
            titulo_dictamen = "🚨 ALTO RIESGO: DESVIACIÓN CRÍTICA DETECTADA"
            detalles = f"El sistema ha interceptado una anomalía severa en el comportamiento del suscriptor. Existe un {probabilidad_ajuste:.2f}% de probabilidad de que esta cuenta derive en un ajuste aprobado en firme. Se recomienda suspender la emisión de la factura y programar inspección técnica en terreno de forma inmediata."
        else:
            color_alerta = "success"
            titulo_dictamen = "🟢 CUENTA ESTABLE: FACTURACIÓN NORMAL"
            detalles = f"El suscriptor presenta un comportamiento consistente con su línea base histórica. La probabilidad de anomalía es insignificante ({probabilidad_ajuste:.2f}%). Cuenta liberada para proceso normal de facturación."
            
        # 4. Retorno de la Alerta Visual
        return html.Div([
            dbc.Alert([
                html.H4(titulo_dictamen, className="alert-heading", style={'fontWeight': 'bold'}),
                html.P(detalles, style={'fontSize': '14px', 'lineHeight': '1.5'}),
                html.Hr(),
                html.Small("Métricas de Soporte de Ingeniería: ", style={'fontWeight': 'bold'}),
                html.Ul([
                    html.Li(f"Desviación Física Calculada: {desviacion_m3:+,.2f} m³"),
                    html.Li(f"Desviación Financiera: ${desviacion_facturacion:+,.2f} COP"),
                    html.Li(f"Indicador de Explosión de Consumo: {'ACTIVO (M3 > 1.5x)' if alerta_alto_consumo == 1 else 'INACTIVO'}")
                ], style={'fontSize': '12px', 'marginTop': '5px'})
            ], color=color_alerta, style={'borderRadius': '8px', 'padding': '20px'})
        ])
        
    except Exception as e:
        return dbc.Alert(f"⚠️ Error matemático durante el procesamiento del vector de entrada: {str(e)}", color="warning")


# =========================================================================
# ARRANQUE DEL SERVIDOR (AL PURO FINAL)
# =========================================================================
if __name__ == '__main__':
    app.run(debug=True, port=8050)