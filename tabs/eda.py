import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from data.data_loader import load_and_clean_data

def obtener_layout_eda():
    """
    Genera dinámicamente el layout del EDA evaluando el dataset real de la preclínica.
    """
    try:
        df = load_and_clean_data()
    except Exception as e:
        return html.Div([dbc.Alert(f"❌ Error al conectar con el almacén de datos CSV: {str(e)}", color="danger")])

    # Saneamiento rápido para consistencia analítica
    df['VALOR_AJUSTE_PERIODO'] = pd.to_numeric(df['VALOR_AJUSTE_PERIODO'], errors='coerce').fillna(0).astype(int)
    df['AJUSTE_EN_ULT_6_MESES'] = pd.to_numeric(df['AJUSTE_EN_ULT_6_MESES'], errors='coerce').fillna(0).astype(int)

    # --- GRÁFICO 1: Proporción Real (Desbalanceo Quirúrgico al 1.28%) ---
    conteo_clases = df['VALOR_AJUSTE_PERIODO'].value_counts().reset_index()
    conteo_clases.columns = ['Estado', 'Total_Usuarios']
    conteo_clases['Estado'] = conteo_clases['Estado'].map({0: 'Sin Ajuste (98.72%)', 1: 'Con Ajuste (1.28%)'})
    
    fig_proporcion = px.pie(
        conteo_clases, values='Total_Usuarios', names='Estado',
        title="<b>Radiografía comercial: El reto del desbalanceo extremo</b>",
        color='Estado', 
        color_discrete_map={'Sin ajuste (98.72%)': '#1e3d59', 'Con ajuste (1.28%)': '#ffc13b'},
        hole=0.4
    )
    fig_proporcion.update_layout(template="plotly_white", margin=dict(t=50, b=20, l=20, r=20), legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"))

    # --- GRÁFICO 2: Desviación de Consumo ---
    df_sample = df.sample(n=min(20000, len(df)), random_state=42)
    fig_desviacion = px.box(
        df_sample, x='VALOR_AJUSTE_PERIODO', y='DESVIACION_M3',
        color='VALOR_AJUSTE_PERIODO',
        title="<b>Impacto de la Desviación de Consumo Físico ($m^3$)</b>",
        color_discrete_map={0: "#1e3d59", 1: "#ffc13b"},
        points=False
    )
    fig_desviacion.update_layout(template="plotly_white", margin=dict(t=50, b=40, l=40, r=40), showlegend=False)
    fig_desviacion.update_xaxes(ticktext=['Cuentas estables (0)', 'Cuentas con ajuste (1)'], tickvals=[0, 1])

    # --- GRÁFICO 3: Análisis de Reincidencia Comercial ---
    df_reincidencia = df.groupby(['AJUSTE_EN_ULT_6_MESES', 'VALOR_AJUSTE_PERIODO']).size().reset_index(name='Cuentas')
    df_reincidencia['Ajuste Semestre Anterior'] = df_reincidencia['AJUSTE_EN_ULT_6_MESES'].map({0: 'Sin Ajustes Previos', 1: 'Con Ajustes Previos'})
    df_reincidencia['Ajuste Mes Actual'] = df_reincidencia['VALOR_AJUSTE_PERIODO'].map({0: 'Estable (0)', 1: 'Requiere Ajuste (1)'})

    fig_reincidencia = px.bar(
        df_reincidencia, x='Ajuste Semestre Anterior', y='Cuentas', color='Ajuste Mes Actual',
        title="<b>Patrón de Reincidencia: Historial Semestral vs Ajuste Actual</b>",
        barmode='group',
        color_discrete_map={'Estable (0)': '#1e3d59', 'Requiere Ajuste (1)': '#ffc13b'},
        text_auto='.2s'
    )
    fig_reincidencia.update_layout(template="plotly_white", margin=dict(t=50, b=40, l=40, r=40), legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))

    # Estructura del Contenedor de Retorno
    return html.Div([
        html.H3("Análisis exploratorio de datos senior - Control de pérdidas", style={'color': '#1e3d59', 'fontWeight': 'bold'}),
        html.P("Visualizaciones estratégicas del universo comercial de 659,856 registros reales.", className="text-muted mb-4"),
        
        dbc.Row([
            dbc.Col([dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_proporcion)])], className="shadow-sm border-0 mb-4")], md=5),
            dbc.Col([dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_reincidencia)])], className="shadow-sm border-0 mb-4")], md=7)
        ]),
        dbc.Row([
            dbc.Col([dbc.Card([dbc.CardBody([dcc.Graph(figure=fig_desviacion)])], className="shadow-sm border-0 mb-4")], md=12)
        ])
    ])