import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os 


# Theme
THEME_COLOR = '#3F72AF'  
SECONDARY_COLOR = '#112D4E'  
BACKGROUND_COLOR = '#F9F7F7'  
PANEL_COLOR = '#DBE2EF'  
TEXT_COLOR = '#333333'  

# Chargement des données
data = pd.read_csv('C:/Users/etudiant/Desktop/projet_Bi/data/DataCoSupplyChainDataset.csv', encoding='ISO-8859-1')


# ventes par catégorie
sales_by_category = data.groupby('Category Name')['Sales'].sum().reset_index()
sales_by_category = sales_by_category.sort_values(by='Sales', ascending=False)

sales_fig = px.bar(
    sales_by_category, 
    x='Category Name', 
    y='Sales', 
    title='Ventes Agrégées par Catégorie',
    color='Sales', 
    color_continuous_scale=['#d3dae5', '#a7b5ca', '#7a90b0', '#4e6b95', '#22467b'],
    template='plotly_white'
)
sales_fig.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Catégorie",
    yaxis_title="Ventes Totales",
    coloraxis_colorbar=dict(title="Ventes"),
    margin=dict(l=40, r=40, t=60, b=40),
)

# commandes par catégorie
orders_by_category = data.groupby(['Category Name'])['Order Id'].count().reset_index(name='Number of Orders')
orders_by_category = orders_by_category.sort_values(by='Number of Orders', ascending=False)

orders_fig = px.bar(
    orders_by_category, 
    x='Category Name', 
    y='Number of Orders', 
    title='Nombre de Commandes par Catégorie', 
    color='Number of Orders', 
    color_continuous_scale=['#d3dae5', '#a7b5ca', '#7a90b0', '#4e6b95', '#22467b'],
    template='plotly_white'
)
orders_fig.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Catégorie",
    yaxis_title="Nombre de Commandes",
    coloraxis_colorbar=dict(title="Commandes"),
    margin=dict(l=40, r=40, t=60, b=40),
)

# Graphiques 
market = data.groupby('Market')['Sales per customer'].sum().reset_index()
market = market.sort_values(by='Sales per customer', ascending=False)

region = data.groupby('Order Region')['Sales per customer'].sum().reset_index()
region = region.sort_values(by='Sales per customer', ascending=False)

fig1 = px.bar(
    market, 
    x='Market', 
    y='Sales per customer', 
    title='Total Sales by Market',
    color='Sales per customer',
    color_continuous_scale=[
    '#d9cce5', '#b299cb', '#8c66b1', '#653397', '#3f007d'
],
    template='plotly_white'
)
fig1.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Market",
    yaxis_title="Sales per Customer",
    coloraxis_colorbar=dict(title="Sales"),
    margin=dict(l=40, r=40, t=60, b=40),
)

fig2 = px.bar(
    region, 
    x='Order Region', 
    y='Sales per customer', 
    title='Total Sales by Region',
    color='Sales per customer',
    color_continuous_scale=[
    '#d9cce5', '#b299cb', '#8c66b1', '#653397', '#3f007d'],
    template='plotly_white'
)
fig2.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Sales per Customer",
    coloraxis_colorbar=dict(title="Sales"),
    margin=dict(l=40, r=40, t=60, b=40),
)

# Graphiques des Pertes 
loss = data[data['Benefit per order'] < 0]
loss_by_category = loss['Category Name'].value_counts().nlargest(10).reset_index()
loss_by_category.columns = ['Category Name', 'Count']

fig_loss1 = px.bar(
    loss_by_category, 
    x='Category Name', 
    y='Count', 
    title='Categories with Most Loss',
    color='Count',
    color_continuous_scale='Reds',
    template='plotly_white'
)
fig_loss1.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Category",
    yaxis_title="Number of Loss Orders",
    coloraxis_colorbar=dict(title="Count"),
    margin=dict(l=40, r=40, t=60, b=40),
)

loss_by_region = loss['Order Region'].value_counts().nlargest(10).reset_index()
loss_by_region.columns = ['Order Region', 'Count']

fig_loss2 = px.bar(
    loss_by_region, 
    x='Order Region', 
    y='Count', 
    title='Regions with Most Loss',
    color='Count',
    color_continuous_scale='Reds',
    template='plotly_white'
)
fig_loss2.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Number of Loss Orders",
    coloraxis_colorbar=dict(title="Count"),
    margin=dict(l=40, r=40, t=60, b=40),
)

# Graphiques des Livrasion
late_delivery_data = data[data['Delivery Status'] == 'Late delivery']
late_by_product = late_delivery_data['Category Name'].value_counts().nlargest(10).reset_index()
late_by_product.columns = ['Category Name', 'Late Deliveries']

late_by_product1 = late_delivery_data['Product Name'].value_counts().nlargest(10).reset_index()
late_by_product1.columns = ['Product Name', 'Late Deliveries']

late_by_region = late_delivery_data['Order Region'].value_counts().nlargest(10).reset_index()
late_by_region.columns = ['Order Region', 'Late Deliveries']

late_by_region_shipment = late_delivery_data.groupby(['Order Region', 'Shipping Mode']).size().reset_index(name='Late Deliveries')
late_by_region_shipment = late_by_region_shipment.sort_values(by='Late Deliveries', ascending=False)


fig_li = px.bar(
    late_by_product,
    x='Category Name',
    y='Late Deliveries',
    title='Top 10 Catégories avec des Livraisons en retard',
    color='Late Deliveries',
    color_continuous_scale=['#d4edda', '#a3d3a1', '#6dbb70', '#3a923d', '#1e6f23'],
    template='plotly_white'
)
fig_li.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,  
    paper_bgcolor=BACKGROUND_COLOR,  
    font_color=TEXT_COLOR,           
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Category",
    yaxis_title="Nombre de livraisons en retard",
    coloraxis_colorbar=dict(title="Late Deliveries"),
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_pro = px.bar(
    late_by_product1,
    x='Product Name',
    y='Late Deliveries',
    title='Top 10 Produits avec des Livraisons en retard',
    labels={'Product Name': 'Product', 'Late Deliveries': 'Late Delivery Count'},
    color='Late Deliveries',
    color_continuous_scale=['#d4edda', '#a3d3a1', '#6dbb70', '#3a923d', '#1e6f23'],
    template='plotly_white'
)

fig_pro.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font_color=TEXT_COLOR,
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Product",
    yaxis_title="Nombre de livraisons en retard",
    coloraxis_colorbar=dict(title="Late Deliveries"),
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_ship = px.bar(
    late_by_region_shipment,
    x='Order Region',
    y='Late Deliveries',
    color='Shipping Mode',
    barmode='group',
    title="Livraisons en retard par Région et Type d'Expédition",
    labels={'Order Region': 'Region', 'Late Deliveries': 'Late Delivery Count'},
    template='plotly_white',
    color_discrete_sequence=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728']
)

fig_ship.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_color='black',
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Number of Late Deliveries",
    margin=dict(l=40, r=40, t=60, b=40)
)

fig_reg = px.bar(
    late_by_region,
    x='Order Region',
    y='Late Deliveries',
    title='Top 10 régions avec Livraisons en retard',
    color='Late Deliveries',
    color_continuous_scale=['#d4edda', '#a3d3a1', '#6dbb70', '#3a923d', '#1e6f23'],
    template='plotly_white'
)

fig_reg.update_layout(
    plot_bgcolor=BACKGROUND_COLOR,  
    paper_bgcolor=BACKGROUND_COLOR,  
    font_color=TEXT_COLOR,          
    title_font_size=20,
    title_x=0.5,
    xaxis_title="Region",
    yaxis_title="Nombre de livraisons en retard",
    coloraxis_colorbar=dict(title="Late Deliveries"),
    margin=dict(l=40, r=40, t=60, b=40)
)

# Custom card component 
def create_card(children, style=None):
    card_style = {
        'backgroundColor': PANEL_COLOR,
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)',
        'padding': '20px',
        'marginBottom': '20px',
    }
    if style:
        card_style.update(style)
    return html.Div(children=children, style=card_style)

app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}],
    assets_folder='assets'
)

# Sidebar 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Img(
                    id='dataco-logo',
                    src='/assets/dataco.png',  
                    style={
                        'width': '150px',
                        'marginBottom': '40px',
                        'marginTop': '20px',
                        'display': 'block',
                        'marginLeft': 'auto',
                        'marginRight': 'auto',
                    }
                ),
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.2)'}),
            html.Ul([
                html.Li([
                    html.Div([
                        html.I(className="fas fa-chart-bar", style={'marginRight': '10px'}),
                        dcc.Link("Ventes et Commandes", href="/", className="sidebar-link")
                    ], className="sidebar-item")
                ]),
                html.Li([
                    html.Div([
                        html.I(className="fas fa-dollar-sign", style={'marginRight': '10px'}),
                        dcc.Link("Ventes Totales", href="/totalsales", className="sidebar-link")
                    ], className="sidebar-item")
                ]),
                html.Li([
                    html.Div([
                        html.I(className="fas fa-exclamation-triangle", style={'marginRight': '10px'}),
                        dcc.Link("Perte", href="/loss", className="sidebar-link")
                    ], className="sidebar-item")
                ]),
                html.Li([
                    html.Div([
                        html.I(className="fas fa-shipping-fast", style={'marginRight': '10px'}),
                        dcc.Link("Livraison", href="/livraison", className="sidebar-link")
                    ], className="sidebar-item")
                ]),
            ], style={
                'listStyleType': 'none',
                'padding': '0',
                'margin': '0',
                'fontSize': '16px',
            }),
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.2)', 'marginTop': '30px'}),
            html.Div([
                html.P("Supply Chain Dashboard", style={'color': 'rgba(255,255,255,0.6)', 'textAlign': 'center', 'fontSize': '12px', 'marginTop': '30px'}),
                html.Img(
                    id='school-logo',
                    src='/assets/ubs.png',  
                    style={
                        'width': '150px',
                        'marginTop': '150px',
                        'marginBottom': '15px',
                        'display': 'block',
                        'marginLeft': 'auto',
                        'marginRight': 'auto',
                    }
                ),
            ])
        ], style={'padding': '20px 10px'})
    ], style={
        'width': '250px',
        'height': '100vh',
        'position': 'fixed',
        'backgroundColor': SECONDARY_COLOR,
        'color': 'white',
        'boxShadow': '2px 0 10px rgba(0, 0, 0, 0.3)',
        'zIndex': '1000',
    }),
    html.Div(id='content', style={
        'marginLeft': '250px',
        'padding': '30px',
        'backgroundColor': BACKGROUND_COLOR,
        'minHeight': '100vh',
    })
], style={
    'fontFamily': '"Roboto", "Segoe UI", "Helvetica Neue", Arial, sans-serif',
    'margin': '0',
    'padding': '0',
})

# CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Supply Chain Dashboard</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: ''' + BACKGROUND_COLOR + ''';
            }
            .sidebar-item {
                padding: 10px 15px;
                border-radius: 5px;
                margin-bottom: 5px;
                transition: background-color 0.3s;
            }
            .sidebar-item:hover {
                background-color: rgba(255,255,255,0.1);
            }
            .sidebar-link {
                color: white;
                text-decoration: none;
                display: block;
            }
            .chart-container {
                transition: transform 0.3s;
            }
            .chart-container:hover {
                transform: translateY(-5px);
            }
            .dashboard-header {
                font-size: 24px;
                font-weight: 500;
                color: ''' + TEXT_COLOR + ''';
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid ''' + THEME_COLOR + ''';
            }
            .card-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            @media (max-width: 1200px) {
                .card-container {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_content(pathname):
    if pathname == '/totalsales':
        return html.Div([
            html.H1("Analyse des Ventes Totales", className="dashboard-header"),
            html.Div([
                create_card([
                    html.H3("Performance du Marché", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='total_sales_market_chart', figure=fig1, className="chart-container")
                    ])
                ]),
                create_card([
                    html.H3("Performance Régionale", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='total_sales_region_chart', figure=fig2, className="chart-container")
                    ])
                ])
            ], className="card-container")
        ])
    
    elif pathname == '/loss':
        return html.Div([
            html.H1("Analyse des Pertes", className="dashboard-header"),
            html.Div([
                create_card([
                    html.H3("Catégories avec Le plus de Pertes", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_category_chart', figure=fig_loss1, className="chart-container")
                    ])
                ]),
                create_card([
                    html.H3("Régions avec Le plus de Pertes", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_region_chart', figure=fig_loss2, className="chart-container")
                    ])
                ])
            ], className="card-container")
        ])
        
    elif pathname == '/livraison':
        return html.Div([
            html.H1("Analyse des Livraisons Tardives", className="dashboard-header"),
            html.Div([
                create_card([
                    html.H3("Top 10 Catégories avec Livraisons Tardives", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_category_chart', figure=fig_li, className="chart-container")
                    ])
                ]),
                create_card([
                    html.H3("Top 10 Produits avec Livraisons Tardives", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_category_chart', figure=fig_pro, className="chart-container")
                    ])
                ]),
                create_card([
                    html.H3("Top 10 Régions avec Livraisons en retard", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_category_chart', figure=fig_reg, className="chart-container")
                    ])
                ]),
                create_card([
                    html.H3("Livraisons en retard par Région et Type d'Expédition", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                    html.Div([
                        dcc.Graph(id='loss_region_chart', figure=fig_ship, className="chart-container")
                    ])
                ])
            ], className="card-container")
        ])
    
    # Defaut page
    return html.Div([
        html.H1("Aperçu des Ventes et des Commandes", className="dashboard-header"),
        html.Div([
            create_card([
                html.H3("Ventes par Catégorie", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                html.Div([
                    dcc.Graph(id='aggregate_sales_chart', figure=sales_fig, className="chart-container")
                ])
            ]),
            create_card([
                html.H3("Commandes par Catégorie", style={'marginBottom': '15px', 'color': SECONDARY_COLOR}),
                html.Div([
                    dcc.Graph(id='aggregate_orders_chart', figure=orders_fig, className="chart-container")
                ])
            ])
        ], className="card-container")
    ])

if __name__ == '__main__':
    app.run(debug=True)
