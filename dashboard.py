"""
Dash Financial Dashboard — Ambuja Cements vs UltraTech Cement
Single-file Dash app (Plotly + Dash + Pandas).
Save as dash_finance_dashboard.py, install dependencies (dash, pandas, plotly) and run.
"""

import pkgutil
if not hasattr(pkgutil, "find_loader"):
    import importlib.util
    pkgutil.find_loader = lambda name: importlib.util.find_spec(name)

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Color maps
metric_colors = {
    'Current Ratio': '#1f77b4',  # dark blue
    'Quick Ratio': '#aec7e8',    # light blue
    'Gross Profit Margin': '#2ca02c',  # green
    'Net Profit Margin': '#98df8a',    # light green
    'Interest Coverage Ratio': '#9467bd',  # purple
    'Inventory Turnover': '#ff7f0e',   # orange
    'Asset Turnover': '#ffbb78',       # light orange
    'Trade Receivable Turnover': '#d62728'  # red
}

company_colors = {
    'Ambuja Cements': '#1f77b4',  # blue
    'UltraTech Cement': '#ff7f0e' # orange
}

# Insights for display
insights = {
    'Current Ratio': "Ambuja’s 1.62 (’21) to 1.55 (’25) shows solid liquidity, peaking at 2.03 (’24), but recent dip hints at tighter operations. UltraTech’s low 0.37–0.44 signals lean liquidity, risking strain but efficient for capital-heavy cement.",
    'Quick Ratio': "Ambuja’s 1.41–1.30 (’21–’25) reflects strong immediate liquidity, though declining. UltraTech’s 0.20–0.17 shows vulnerability, prioritizing efficiency over cash reserves.",
    'Gross Profit Margin': "Ambuja’s volatile 17.46% (’21) to 9.96% (’25) suggests cost pressures, recovering to 14.40% (’24). UltraTech’s robust 56.22%–49.03% showcases superior pricing power and scale.",
    'Net Profit Margin': "Ambuja improves from 6.25% (’22) to 11.89% (’25), signaling better cost control. UltraTech peaks at 13.69% (’22) but falls to 8.47% (’25), indicating moderated profitability.",
    'Interest Coverage Ratio': "Ambuja’s strong 37.14–28.46 (’21–’25) reflects low debt risk. UltraTech’s 7.31–6.67 suggests higher leverage but manageable coverage.",
    'Inventory Turnover': "Ambuja’s 10.58–8.25 (’21–’25) shows slowing inventory movement, risking costs. UltraTech’s 5.59–4.41 (’22–’25) indicates even slower turnover, less efficient.",
    'Asset Turnover': "Ambuja’s 0.94–0.61 (’21–’25) reflects declining asset efficiency. UltraTech’s 0.86–0.92 (’22–’25) is steadier, slightly outperforming in sales generation.",
    'Trade Receivable Turnover': "Ambuja’s 48.00–25.00 (’21–’25) signals slower collections, risking cash flow. UltraTech’s 2.54–2.28 (’22–’25) is far slower, highlighting credit leniency."
}

# ----- Data (user-provided) -----
years = ['Mar-21', 'Mar-22', 'Mar-23', 'Mar-24', 'Mar-25']
year_numbers = [2021, 2022, 2023, 2024, 2025]

ambuja = {
    'Current Ratio': [1.62, 1.42, 1.96, 2.03, 1.55],
    'Quick Ratio': [1.41, 1.22, 1.72, 1.79, 1.30],
    'Gross Profit Margin': [17.46, 8.35, 8.93, 14.40, 9.96],
    'Net Profit Margin': [9.59, 6.25, 6.63, 10.78, 11.89],
    'Interest Coverage Ratio': [37.14, 19.33, 21.63, 21.50, 28.46],
    'Inventory Turnover': [10.58, 9.26, 11.90, 9.19, 8.25],
    'Asset Turnover': [0.94, 0.95, 1.09, 0.74, 0.61],
    'Trade Receivable Turnover': [48.00, 36.51, 43.26, 28.01, 25.00]
}

ultratech = {
    'Current Ratio': [0.37, 0.39, 0.42, 0.43, 0.44],
    'Quick Ratio': [0.20, 0.14, 0.17, 0.15, 0.17],
    'Gross Profit Margin': [56.22, 50.97, 45.01, 48.87, 49.03],
    'Net Profit Margin': [12.30, 13.69, 7.86, 9.97, 8.47],
    'Interest Coverage Ratio': [7.31, 11.37, 10.62, 11.71, 6.67],
    'Inventory Turnover': [None, 5.59, 6.00, 4.97, 4.41],
    'Asset Turnover': [None, 0.86, 1.01, 1.07, 0.92],
    'Trade Receivable Turnover': [None, 2.54, 2.58, 2.55, 2.28]
}

# Build tidy dataframe
rows = []
for i, y in enumerate(years):
    for k, v in ambuja.items():
        rows.append({'Company': 'Ambuja Cements', 'Metric': k, 'Value': v[i], 'YearLabel': y, 'Year': year_numbers[i]})
    for k, v in ultratech.items():
        rows.append({'Company': 'UltraTech Cement', 'Metric': k, 'Value': v[i], 'YearLabel': y, 'Year': year_numbers[i]})
df = pd.DataFrame(rows)

# Metric groups for UI
metric_groups = {
    'liquidity': ['Current Ratio', 'Quick Ratio'],
    'profitability': ['Gross Profit Margin', 'Net Profit Margin'],
    'turnover': ['Inventory Turnover', 'Asset Turnover', 'Trade Receivable Turnover'],
    'leverage': ['Interest Coverage Ratio']
}

# Helper to fetch latest KPI
def kpi_latest(df_local, company, metric):
    sub = df_local[(df_local['Company'] == company) & (df_local['Metric'] == metric)]
    if sub.empty: 
        return None
    return sub.sort_values('Year')['Value'].iloc[-1]

# ----- Dash app -----
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(style={'font-family': 'Inter, Arial, sans-serif', 'padding': '18px'}, children=[
    html.H2("Financial Dashboard — Ambuja Cements vs UltraTech Cement"),
    html.Div("Compare liquidity, profitability, leverage, and turnover metrics (Mar-21 → Mar-25).", style={'color': '#666'}),

    # Controls
    html.Div(style={'display': 'flex', 'gap': '12px', 'align-items': 'center', 'margin-top': '12px'}, children=[
        html.Div([
            html.Label("Company"),
            dcc.Dropdown(
                id='company-select',
                options=[
                    {'label': 'Ambuja Cements', 'value': 'Ambuja Cements'},
                    {'label': 'UltraTech Cement', 'value': 'UltraTech Cement'},
                    {'label': 'Both Companies', 'value': 'Both'}
                ],
                value='Both',
                clearable=False,
                style={'width': '260px'}
            )
        ]),
        html.Div([
            html.Label("Metric group"),
            dcc.Dropdown(
                id='metric-group',
                options=[
                    {'label': 'Liquidity Ratios', 'value': 'liquidity'},
                    {'label': 'Profitability Ratios', 'value': 'profitability'},
                    {'label': 'Leverage Ratios', 'value': 'leverage'},
                    {'label': 'Turnover Ratios', 'value': 'turnover'}
                ],
                value='liquidity',
                clearable=False,
                style={'width': '260px'}
            )
        ]),
        html.Div(style={'min-width': '280px'}, children=[
            html.Label("Year range"),
            dcc.RangeSlider(
                id='year-range',
                min=min(year_numbers),
                max=max(year_numbers),
                value=[min(year_numbers), max(year_numbers)],
                marks={y: str(y) for y in year_numbers},
                step=None,
                tooltip={'placement': 'bottom'}
            )
        ])
    ]),

    # Executive summary KPI cards container (populated by callback)
    html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '12px', 'flex-wrap': 'wrap', 'margin-top': '16px'}),

    # Insights section
    html.Div(id='insights-section', style={'margin-top': '24px', 'padding': '12px', 'border': '1px solid #e6e6e6', 'border-radius': '8px', 'background': '#f9f9f9'}),

    # Main chart + right pane
    html.Div(style={'display': 'flex', 'gap': '18px', 'margin-top': '18px'}, children=[
        html.Div(dcc.Graph(id='main-chart', config={'displayModeBar': True}, style={'min-width': '640px', 'height': '560px'}), style={'flex': '1 1 70%'}),
        html.Div(style={'flex': '0 0 360px'}, children=[
            html.H4("Mini-trend & data"),
            dcc.Graph(id='spark-chart', config={'displayModeBar': False}, style={'height': '280px', 'margin-bottom': '20px'}),
            html.Div(id='data-table', style={'margin-top': '12px', 'font-size': '13px', 'white-space': 'pre-wrap', 'font-family': 'monospace', 'overflow-y': 'auto', 'max-height': '200px'})
        ])
    ]),

    html.Div(style={'margin-top': '12px', 'color': '#999', 'font-size': '12px'}, children=[
        html.Span("Data source: user-provided values (Mar-21 → Mar-25).")
    ])
])

# ----- Callbacks -----
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('insights-section', 'children')],
    [Input('company-select', 'value'),
     Input('metric-group', 'value')]
)
def update_kpis_and_insights(company, group):
    metrics = metric_groups.get(group, [])

    cards = []
    for metric in metrics:
        if company == 'Both':
            a_val = kpi_latest(df, 'Ambuja Cements', metric)
            u_val = kpi_latest(df, 'UltraTech Cement', metric)
            body = html.Div([
                html.Div(metric, style={'font-size': '12px', 'color': '#333'}),
                html.Div(style={'display':'flex','gap':'10px','margin-top':'6px'}, children=[
                    html.Div([html.Div("Ambuja", style={'font-size':'11px','color':'#666'}), html.Div(f"{a_val:.2f}" if a_val is not None else "—", style={'font-weight':'700'})]),
                    html.Div([html.Div("UltraTech", style={'font-size':'11px','color':'#666'}), html.Div(f"{u_val:.2f}" if u_val is not None else "—", style={'font-weight':'700'})])
                ])
            ], style={'padding': '8px'})
        else:
            val = kpi_latest(df, company, metric)
            body = html.Div([
                html.Div(metric, style={'font-size': '12px', 'color': '#333'}),
                html.Div(f"{val:.2f}" if val is not None else "—", style={'font-size': '18px', 'font-weight': '700', 'margin-top': '6px'})
            ], style={'padding': '8px'})
        card = html.Div(body, style={
            'border': '1px solid #e6e6e6', 'border-radius': '8px',
            'min-width': '170px', 'background': '#fff', 'box-shadow': '0 1px 3px rgba(0,0,0,0.04)'
        })
        cards.append(card)

    # Insights for selected group
    insight_children = [html.H4("Insights for Selected Ratios")]
    for metric in metrics:
        insight_children.append(html.Div([
            html.Strong(metric + ": "),
            insights.get(metric, "No insight available.")
        ], style={'margin-bottom': '8px'}))

    return cards, insight_children

@app.callback(
    [Output('main-chart', 'figure'),
     Output('spark-chart', 'figure'),
     Output('data-table', 'children')],
    [Input('company-select', 'value'),
     Input('metric-group', 'value'),
     Input('year-range', 'value')]
)
def update_charts(company, group, year_range):
    yr_min, yr_max = year_range
    metrics = metric_groups[group]
    # Filtered DF
    dff = df[(df['Metric'].isin(metrics)) & (df['Year'] >= yr_min) & (df['Year'] <= yr_max)]

    # Main chart
    fig = go.Figure()
    if company == 'Both':
        for metric in metrics:
            for comp in ['Ambuja Cements', 'UltraTech Cement']:
                s = dff[(dff['Metric'] == metric) & (dff['Company'] == comp)].sort_values('Year')
                marker = dict(color=metric_colors.get(metric, '#000000'))
                if comp == 'UltraTech Cement':
                    marker['pattern'] = dict(shape="/", fillmode="overlay", fgcolor="white", fgopacity=0.3)
                fig.add_trace(go.Bar(
                    x=s['YearLabel'],
                    y=s['Value'],
                    name=f"{comp} — {metric}",
                    text=[f"{v:.2f}" if v is not None else "—" for v in s['Value']],
                    textposition='auto',
                    marker=marker
                ))
        fig.update_layout(barmode='group', title="Comparison — grouped by metric & company", xaxis_title="Year", yaxis_title="Value")
    else:
        for metric in metrics:
            s = dff[(dff['Company'] == company) & (dff['Metric'] == metric)].sort_values('Year')
            marker = dict(color=metric_colors.get(metric, '#000000'))
            fig.add_trace(go.Bar(
                x=s['YearLabel'],
                y=s['Value'],
                name=metric,
                text=[f"{v:.2f}" if v is not None else "—" for v in s['Value']],
                textposition='auto',
                marker=marker
            ))
        fig.update_layout(barmode='group', title=f"{company} — {group.title()}", xaxis_title="Year", yaxis_title="Value")

    # Sparkline (first metric)
    spark = go.Figure()
    primary = metrics[0]
    if company == 'Both':
        for comp in ['Ambuja Cements', 'UltraTech Cement']:
            s = dff[(dff['Metric'] == primary) & (dff['Company'] == comp)].sort_values('Year')
            spark.add_trace(go.Scatter(x=s['YearLabel'], y=s['Value'], mode='lines+markers', name=comp, line=dict(color=company_colors.get(comp, '#000000'))))
    else:
        s = dff[(dff['Metric'] == primary) & (dff['Company'] == company)].sort_values('Year')
        spark.add_trace(go.Scatter(x=s['YearLabel'], y=s['Value'], mode='lines+markers', name=company, line=dict(color=company_colors.get(company, '#000000'))))

    spark.update_layout(title=f"Trend — {primary}", margin={'t':30, 'b':20, 'l':30, 'r':10}, height=280)

    # Data table (CSV text)
    table_df = dff.pivot_table(index='YearLabel', columns=['Company', 'Metric'], values='Value')
    table_text = table_df.round(3).to_csv()
    return fig, spark, html.Pre(table_text)

if __name__ == "__main__":
    # Option 1: Debug mode off (safe)
    app.run(debug=False)