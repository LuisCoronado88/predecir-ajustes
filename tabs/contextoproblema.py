from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H3("Contexto comercial y objetivos del proyecto", className="text-primary mb-4"),
    
    # Fila de Alerta / Diagnóstico Comercial
    dbc.Alert([
        html.H5("El reto de la facturación y el Control de ingresos", className="alert-heading font-weight-bold"),
        html.P(
            "En las empresas de servicios públicos domiciliarios (Acueducto y Alcantarillado), las desviaciones extremas de consumo "
            "provocan reclamaciones masivas. Cuando una anomalía física o error de lectura es procedente, se genera un Ajuste de Facturación (Clase 1). "
            "Interceptar estas anomalías en la etapa de precrítica comercial evita pérdidas millonarias por descapitalización y reprocesos administrativos.",
            className="mb-0"
        )
    ], color="warning", className="shadow-sm border-0 mb-4"),

    # Pilares del Problema (Cards)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📉 Impacto Financiero", className="text-white m-0"), className="bg-danger"),
                dbc.CardBody([
                    html.P(
                        "Cada ajuste aprobado de forma reactiva representa un retraso directo en el recaudo del periodo. "
                        "El desbalanceo extremo de la operación muestra que la Clase 1 representa solo el 1.28% del universo comercial, "
                        "lo que exige una precisión matemática absoluta para no quebrar la viabilidad financiera del control de pérdidas.",
                        className="card-text text-muted"
                    )
                ])
            ], className="shadow-sm border-0 h-100")
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("⏳ Restricción Operativa", className="text-white m-0"), className="bg-secondary"),
                dbc.CardBody([
                    html.P(
                        "Analizar un universo de 659,856 registros buscando anomalías críticas es humanamente imposible. "
                        "Los modelos lineales tradicionales colapsan operativamente generando más de 97,000 falsas alarmas, "
                        "por lo que se requiere una arquitectura no lineal quirúrgica para dirigir eficientemente los recursos de terreno.",
                        className="card-text text-muted"
                    )
                ])
            ], className="shadow-sm border-0 h-100")
        ], md=6),
    ], className="mb-4"),

    # Objetivos Centrales de AjustePredictor
    dbc.Card([
        dbc.CardBody([
            html.H5("Objetivos estratégicos de Ajuste predictor", className="text-primary mb-3"),
            html.Ol([
                html.Li([
                    html.Strong("Predecir con enfoque de ensamble: "), 
                    "Implementar algoritmos secuenciales basados en árboles (Gradient Boosting Classifier) para capturar picos físicos bruscos e interacciones complejas de consumo."
                ], className="mb-2 text-muted"),
                html.Li([
                    html.Strong("Optimizar el gasto logístico: "), 
                    "Mitigar drásticamente las falsas alarmas comerciales, garantizando que el equipo de inspección técnica verifique únicamente las cuentas con un riesgo real superior al umbral crítico."
                ], className="mb-2 text-muted"),
                html.Li([
                    html.Strong("Sustentación Científica y ROI: "), 
                    "Garantizar la viabilidad del proyecto maximizando el F1-Score como métrica reina de selección, logrando un balance óptimo entre la detección de pérdidas y el costo operativo."
                ], className="mb-2 text-muted"),
            ])
        ])
    ], className="shadow-sm border-0 mb-4")
], className="tab-content-padding")