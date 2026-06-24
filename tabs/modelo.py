import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

def obtener_layout_modelo():
    """
    Renderiza de forma aislada la interfaz interactiva para simulaciones 
    en tiempo real usando el Pipeline del Gradient Boosting.
    """
    return html.Div([
        html.H3("Simulador de ajuste de facturacion", style={'color': '#1e3d59', 'fontWeight': 'bold'}),
        html.P("Ingrese las métricas comerciales operativas actuales del suscriptor para calcular la probabilidad predictiva de ajuste técnico.", className="text-muted mb-4"),
        
        dbc.Row([
            # Columna del Formulario de Parámetros
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Consumo del Periodo Actual ($m^3$):", style={'fontWeight': '600'}),
                        dcc.Input(id='sim-m3-periodo', type='number', value=25, className="form-control mb-3"),
                        
                        html.Label("Consumo Histórico Promedio ($m^3$):", style={'fontWeight': '600'}),
                        dcc.Input(id='sim-m3-promedio', type='number', value=20, className="form-control mb-3"),
                        
                        html.Label("Facturación del Periodo Actual (COP):", style={'fontWeight': '600'}),
                        dcc.Input(id='sim-fact-periodo', type='number', value=130000, className="form-control mb-3"),
                        
                        html.Label("Facturación Histórica Promedio (COP):", style={'fontWeight': '600'}),
                        dcc.Input(id='sim-fact-promedio', type='number', value=110000, className="form-control mb-3"),
                        
                        html.Label("¿Presentó ajustes en los últimos 6 meses?:", style={'fontWeight': '600'}),
                        dcc.Dropdown(id='sim-ajustes-previos', options=[
                            {'label': 'No presenta antecedentes (0)', 'value': 0},
                            {'label': 'Sí, presenta historial de ajustes (1)', 'value': 1}
                        ], value=0, className="mb-4", clearable=False),
                        
                        html.Button("🚀 Ejecutar Inferencia de Modelamiento", id="btn-simular", className="btn btn-primary w-100", style={'backgroundColor': '#1e3d59', 'border': 'none', 'fontWeight': 'bold'})
                    ])
                ], className="shadow-sm border-0")
            ], md=5),
            
            # Columna del Bloque del Dictamen de Resultados
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📋 Dictamen Técnico Automático", style={'color': '#1e3d59', 'fontWeight': '600'}),
                        html.Hr(),
                        html.Div(id='resultado-simulacion', children=[
                            html.Div("Ingrese los parámetros a la izquierda y presione el botón de simulación.", className="text-muted style={'fontStyle': 'italic'}")
                        ])
                    ])
                ], className="shadow-sm border-0 h-100", style={'backgroundColor': '#ffffff'})
            ], md=7)
        ])
    ])