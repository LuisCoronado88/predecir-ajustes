from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Metodología de Ingeniería de Datos y Modelado", className="text-primary mb-4"),
    html.P(
        "Para garantizar que el modelo no memorice los datos (overfitting) y responda con total fiabilidad en producción, "
        "diseñamos un flujo metodológico senior dividido en cuatro fases estrictas:",
        className="text-muted mb-4"
    ),

    # Fases del Flujo Metodológico (Estructura de Bloques Secuenciales)
    dbc.Row([
        # Fase 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 1", className="badge bg-primary text-white mb-2"),
                    html.H5("Ingesta y Saneamiento", className="text-dark font-weight-bold"),
                    html.P(
                        "Procesamiento del universo comercial (659,856 registros). Corrección de formatos decimales latinos, "
                        "control de nulos mediante imputación estratégica e implementación de suelos en cero (0) para neutralizar valores negativos.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 2", className="badge bg-info text-white mb-2"),
                    html.H5("Ingeniería de Características", className="text-dark font-weight-bold"),
                    html.P(
                        "Creación de variables sintéticas de negocio basadas en vectores de dirección no lineales: DESVIACION_M3, "
                        "DESVIACION_FACTURACION y el flag ALERTA_ALTO_CONSUMO para capturar saltos abruptos en el comportamiento del usuario.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 3
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 3", className="badge bg-warning text-dark mb-2"),
                    html.H5("Validación Cruzada", className="text-dark font-weight-bold"),
                    html.P(
                        "Estrategia Stratified 5-Fold. Dividimos el dataset en 5 bloques, garantizando que el desbalanceo extremo "
                        "de la Clase 1 (1.28%) se mantenga homogéneo en cada pliegue, asegurando evaluaciones robustas y honestas.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),

        # Fase 4
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("FASE 4", className="badge bg-success text-white mb-2"),
                    html.H5("Optimización F1-Score", className="text-dark font-weight-bold"),
                    html.P(
                        "Competencia de arquitecturas enfocada en mitigar falsos positivos. Coronamos a Gradient Boosting como algoritmo final "
                        "al multiplicar por cuatro el rendimiento del Baseline lineal, alcanzando una Precision quirúrgica del 57.67%.",
                        className="small text-muted"
                    )
                ])
            ], className="shadow-sm border-0 mb-3 h-100")
        ], md=3),
    ], className="mb-4"),

    # Recuadro Técnico de Arquitectura de Software
    dbc.Card([
        dbc.CardHeader(html.H6("⚙️ Arquitectura de Software del Pipeline de Producción", className="m-0 font-weight-bold")),
        dbc.CardBody([
            html.P(
                "La solución se consolida mediante un Pipeline serializado físico (.pkl). Al integrar un ColumnTransformer de scikit-learn, "
                "el preprocesamiento numérico (MinMaxScaler) y categórico (OneHotEncoder) queda empaquetado de forma indivisible junto con el "
                "clasificador Gradient Boosting. Esto permite que la interfaz Dash consuma el modelo de manera desacoplada en un solo paso, "
                "garantizando la inmunidad del sistema ante cambios de tipos de datos en la carga mensual.",
                className="card-text small text-muted", style={"text-align": "justify"}
            )
        ], className="bg-light")
    ], className="border-0 shadow-sm")
], className="tab-content-padding")