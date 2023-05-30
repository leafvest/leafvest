from math import e
import os
import re

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.validator_cache # need to solve circular dependency

import pandas as pd
import yfinance as yf

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# --------------------------------------------------------
# Load Data
# --------------------------------------------------------
company_info_data = pd.read_csv('data/company_info.csv')
company_description_data = pd.read_csv('data/company_description.csv')
company_esg_scores_data = pd.read_csv('data/company_refinitiv_esg.csv')
company_fin_info_data = pd.read_csv('data/company_fin_info.csv')
industries = pd.read_csv('data/industry.csv')
industry_names = list(industries['Industry'])
industry_options = []
for name in industry_names:
    entry = {'label': name, 'value': name}
    industry_options.append(entry)
sectors = pd.read_csv('data/sector.csv')
sector_names = list(sectors['Sector'])
sector_options = []
for name in sector_names:
    entry = {'label': name, 'value': name}
    sector_options.append(entry)

# emission data 
facility_info_data = pd.read_csv('data/facility_info.csv')
facility_ghg_data = pd.read_csv('data/facility_ghg.csv')
facility_company_year_data = pd.read_csv('data/facility_company_year.csv')



# --------------------------------------------------------
# Basic Dash App Info
# --------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'leafvest'
server = app.server
suppress_callback_exceptions=True
logo_src = os.getcwd() + '/assets/leafvest.png'


LOGO_HEIGHT = 100
LOGO_HEIGHT_MAX = 100


# --------------------------------------------------------
# Global Layout
# --------------------------------------------------------
app.layout = html.Div([    
    html.Div([ 
        # Logo
        html.Div([
            html.Img(src=app.get_asset_url('leafvest.png'), 
                     height=LOGO_HEIGHT,
                     style={"padding": "25px"}),
        ], className="one columns"),
        
        # Company Name and Slogan
        html.Div([ 
            html.H2('Leafvest', style={"font-family": "Trebuchet MS", 'color': '#1A9968', "marginTop": "35px"}),
            html.H5('invest in green', style={"font-family": "Trebuchet MS", "marginTop": "-20px"})
        ], className="two columns"),
        
        # Tabs
        html.Div([ 
            dcc.Tabs(id="tabs", value='main-tab', children=[
                dcc.Tab(label='Main', value='main-tab',
                        style={'font-weight': 'bold'},
                        selected_style={'font-weight': 'bold', 
                                        'color': '#1A9968', 
                                        'borderTop': '2px solid #1A9968'}),
                
                dcc.Tab(label='Company', value='company-tab',
                        style={'font-weight': 'bold'},
                        selected_style={'font-weight': 'bold', 
                                        'color': '#1A9968', 
                                        'borderTop': '2px solid #1A9968'}),
                
                dcc.Tab(label='Company VS Company', value='company-vs-tab',
                        style={'font-weight': 'bold'},
                        selected_style={'font-weight': 'bold', 
                                        'color': '#1A9968', 
                                        'borderTop': '2px solid #1A9968'}),
                
                dcc.Tab(label='Industry', value='industry-tab',
                        style={'font-weight': 'bold'},
                        selected_style={'font-weight': 'bold', 
                                        'color': '#1A9968', 
                                        'borderTop': '2px solid #1A9968'}),
                
                dcc.Tab(label='Sector', value='sector-tab',
                        style={'font-weight': 'bold'},
                        selected_style={'font-weight': 'bold', 
                                        'color': '#1A9968', 
                                        'borderTop': '2px solid #1A9968'}),
            ], style={"padding-top": "45px", "padding-right": "200px"}),
        ], className="nine columns")
    ], className="row"),
    
    # Line Divider
    html.Div([html.Hr()], 
    className="row", 
    style={'padding-left': '25px', 
           'padding-right': '25px',
           'marginTop': '-30px',
           'marginBottom': '-30px'}),
    
    # Chosen Page (Main, Company, etc.)
    html.Div([html.Div(id='tabs-content')], 
    className="row", 
    style={"padding-top": "10px",
           "padding-left": "50px",
           "padding-right": "50px"}),
])


# --------------------------------------------------------
# Main Page Layout
# --------------------------------------------------------
def main_view():
    return html.Div([
        # Page Description, Row 0
        html.Div([ 
            html.Div([ 
                html.P('GreenVest collects and dive deep into companies’ financial and greenhouse data to generate data-driven insights into companies’ environmental, social and governance initiatives. Our App can help facilitate investment process to whom are seeking both financial returns and social/environment good to bring about social change regarded as positive proponent.', style={'color': '#808080'}),
            ], className="twelve columns")
        ], className="row"),
        
        # Figures, Row 1
        html.Div([
            # Scatter Plot
            html.Div([
                html.Div([
                    html.Div(id='main_scatter')
                ], className='row'),
                
                # X Value Picker
                html.Div([
                    html.Div([
                        html.P('X values:'),
                    ], className='two columns'),
                    html.Div([
                        dcc.Dropdown(
                            id='main_x_scatter_input',
                            value='co2',
                            options=[{'label': 'Carbon Dioxide (CO2)', 'value': 'co2'},
                                     {'label': 'Nitrous (N2O)', 'value': 'n2o'},
                                     {'label': 'Methane (CH4)', 'value': 'ch4'}]),
                    ], className='five columns'),
                ], className='row'),
                
                # Y Value Picker
                html.Div([
                    html.Div([
                        html.P('Y values:'),
                    ], className='two columns'),
                    html.Div([
                        dcc.Dropdown(
                            id='main_y_scatter_input',
                            value='Market Cap',
                            options=[{'label': 'Market Cap', 'value': 'Market Cap'},
                                    {'label': 'Volume', 'value': 'Volume'}]),
                    ], className='five columns'),
                ], className='row'),
                
                # Enity Value Picker
                html.Div([
                    html.Div([
                        html.P('For:'),
                    ], className='two columns'),
                    html.Div([
                        dcc.Dropdown(
                            id='entities_scatter_input',
                            value='Symbol',
                            options=[{'label': 'Company', 'value': 'Symbol'},
                                    {'label': 'Sector', 'value': 'Sector'},
                                    {'label': 'Industry', 'value': 'Industry'}]),
                    ], className='five columns'),
                ], className='row'),
            ], className="six columns"),
            
            # Ranking Table
            html.Div([
                html.Div(id='main_table'),
                html.P('Criteria:'),
                dcc.Dropdown(
                    id='main_table_input_criteria',
                    value=['ESG Score', 'eps_ratio'], 
                    multi=True,
                    options=[
                    {'label': 'ESG Score', 'value': 'ESG Score'},
                    {'label': 'Environment', 'value': 'Environment'},
                    {'label': 'Social', 'value': 'Social'},
                    {'label': 'Governance', 'value': 'Governance'},
                    {'label': 'EPS ratio', 'value': 'eps_ratio'},
                    {'label': 'P/E ratio', 'value': 'pe_ratio'},
                    {'label': 'PEG ratio', 'value': 'peg_ratio'},
                    {'label': 'P/S ratio', 'value': 'ps_ratio'},
                    {'label': 'P/B ratio', 'value': 'pb_ratio'}
                ]),
            ], className="six columns")
        ], className="row"),
    ])
    

# --------------------------------------------------------
# Callbacks for Main Page
# --------------------------------------------------------
@app.callback(Output('main_scatter', 'children'),
              Input('main_x_scatter_input', 'value'),
              Input('main_y_scatter_input', 'value'),
              Input('entities_scatter_input', 'value'),)
def show_all_companies_scatter_plot(x_input, y_input, entities) -> None:
    """Scatter plot of Financial Data vs Green Data on main page"""
    data = pd.merge(left=facility_info_data, 
                    right=facility_company_year_data, 
                    left_on='Facility Gov ID', 
                    right_on='Facility Gov ID')
    data = pd.merge(left=data,
                    right=company_info_data, 
                    left_on='Symbol', 
                    right_on='Symbol')
    data = pd.merge(left=data, 
                    right=facility_ghg_data, 
                    left_on='Facility Gov ID', 
                    right_on='Facility Gov ID')
    if entities == 'Symbol':
        data = data.groupby(['Symbol', 'Name', 'Sector', 'GHG Year']).sum()
        data.reset_index(inplace=True)
        fig = px.scatter(data, 
                    x=x_input, 
                    y=y_input, 
                    animation_frame="GHG Year", 
                    animation_group="Symbol",
                    size="Market Cap", 
                    color="Sector", 
                    hover_name="Name",
                    size_max=100,
                    log_x=True,
                    log_y=True,
                    height=600)
    elif entities == 'Sector':
        data = data.groupby(['Sector', 'GHG Year']).sum()
        data.reset_index(inplace=True)
        fig = px.scatter(data, 
                    x=x_input, 
                    y=y_input, 
                    animation_frame="GHG Year", 
                    animation_group="Sector",
                    size="Market Cap", 
                    color="Sector", 
                    hover_name="Sector",
                    size_max=100,
                    log_x=True,
                    log_y=True,
                    height=600)
    elif entities == 'Industry':
        data = data.groupby(['Industry', 'GHG Year']).sum()
        data.reset_index(inplace=True)
        fig = px.scatter(data, 
                    x=x_input, 
                    y=y_input, 
                    animation_frame="GHG Year", 
                    animation_group="Industry",
                    size="Market Cap", 
                    color="Industry", 
                    hover_name="Industry",
                    size_max=100,
                    log_x=True,
                    log_y=True,
                    height=600)
    fig.update_layout(title_text='Sustainability Investing Insights', 
                      title_x=0.5)
    return dcc.Graph(figure=fig)


@app.callback(Output('main_table', 'children'),
              Input('main_table_input_criteria', 'value'))
def show_table(criteria):
    """Table for ranking of all Companies on the main page"""
    try:
        combined = pd.merge(left=company_esg_scores_data,
                            right=company_info_data,
                            on='Symbol')
        combined = pd.merge(left=combined,
                            right=company_fin_info_data,
                            on='Symbol')
        combined = combined.round(1)
        table = combined[['Symbol', 'ESG Score', 'Environment', 'Social', 'Governance', 'peg_ratio', 'eps_ratio', 'pb_ratio', 'ps_ratio','pe_ratio']]
        table = table.sort_values(by=criteria, ascending=False).head(20)
    except:
        return html.Div()
    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(table.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[table['Symbol'], table['ESG Score'], table['Environment'], table['Social'],
                            table['Governance'], table['peg_ratio'], table['eps_ratio'], table['pb_ratio'], 
                            table['ps_ratio'],table['pe_ratio']]))
            ])
        fig.update_layout(title_text='Top 20 Companies for Sustainibility Investing', 
                        title_x=0.5)
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Company VS Company Page Layout
# --------------------------------------------------------
def company_vs_view():
    return html.Div([
        # Top Row 0
        html.Div([
            # Gas Picker
            html.H6('Gas: '),
            dcc.Dropdown(
                id='company_vs_gas',
                options=[
                    {'label': 'Carbon Dioxide (CO2)', 'value': 'co2'},
                    {'label': 'Methane (CH4)', 'value': 'ch4'},
                    {'label': 'Nitrous (N2O)', 'value': 'n2o'}
                ],
                value='co2'
            ),
        ], className="row"),
        
        # Next Row 1
        html.Div([
            # Left Company
            html.Div([
                # Symbol Picker
                html.Div([
                    html.H6('Symbol: '),
                    dcc.Input(id='company_vs_left_symbol',
                            type='text',
                            value='TSLA'),
                    html.P("^ enter company's ticker", style={'color': 'grey'})
                ], className="row"),
                
                html.Div([
                    html.H3(id='company_vs_left_name'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_left_esg'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_left_ratios'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_left_emissions'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_left_emission_map'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_left_facilities_map'),
                ], className="row"),
            ], className="six columns"),
            
            # Right Company
            html.Div([
                # Symbol Picker
                html.Div([
                    html.H6('Symbol: '),
                    dcc.Input(id='company_vs_right_symbol',
                              type='text',
                              value='F'),
                    html.P("^ enter company's ticker", style={'color': 'grey'})
                ], className="row"),
                
                html.Div([
                    html.H3(id='company_vs_right_name'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_right_esg'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_right_ratios'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_right_emissions'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_right_emission_map'),
                ], className="row"),
                
                html.Div([
                    html.Div(id='company_vs_right_facilities_map'),
                ], className="row"),
            ], className="six columns"),
        ], className="row")
    ])
    

# --------------------------------------------------------
# Callbacks for Left Company on Company VS Page
# --------------------------------------------------------
@app.callback(Output('company_vs_left_name', 'children'),
              Input('company_vs_left_symbol', 'value'))
def company_vs_left_name(symbol):
    """Name of the Left Company on Company VS page"""
    try:
        symbol = symbol.upper()
        name = company_info_data[
            company_info_data['Symbol'] == symbol
        ].iloc[0,1]
    except:
        return 'No company found'
    else:  
        name = name.replace('Common Stock', '')
        name = name.replace('Shares', '')
        name = name.replace('Ordinary Shares', '')
        return name


@app.callback(Output('company_vs_left_esg', 'children'),
              Input('company_vs_left_symbol', 'value'))
def company_vs_left_esg(symbol):
    """Figure of Left Company ESG Scores on Company VS page"""
    try:
        l  = symbol.split(',')
        df = company_esg_scores_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        character = ['ESG Score', 
                    'Environment', 'Emissions', 'Resource Use', 'Innovation',
                    'Social', 'Human Rights', 'Product Responsibility', 'Workforce', 'Community',
                    'Governance', 'Management', 'Shareholders', 'CSR Strategy']
        parent = ['', 
                'ESG Score', 'Environment', 'Environment', 'Environment', 
                'ESG Score', 'Social', 'Social', 'Social', 'Social',
                'ESG Score', 'Governance', 'Governance', 'Governance']
        value = [df.iloc[0,2], 
                df.iloc[0,3], df.iloc[0,4], df.iloc[0,5], df.iloc[0,6],
                df.iloc[0,7], df.iloc[0,8], df.iloc[0,9], df.iloc[0,10], df.iloc[0,11],
                df.iloc[0,12], df.iloc[0,13], df.iloc[0,14], df.iloc[0,15]]
        labels = { character[i]: value[i] for i in range(len(character)) }
        data = {
            'character': character,
            'parent': parent,
            'value': value
        }
        fig = px.sunburst(
            data,
            names='character',
            values='value',
            parents='parent',
            title='ESG Breakdown',
            labels=labels,
            height=600
        )   
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_left_ratios', 'children'),
              Input('company_vs_left_symbol', 'value'))
def show_vs_left_ratios(symbol):
    """Figure of Left Company Financial Ratios on Company VS page"""
    try:
        l = symbol.split(',')
        df = company_fin_info_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(
            rows=1, 
            cols=5, 
            shared_xaxes=True,
            subplot_titles=("P/E ratio", "PEG ratio", "EPS ratio", "P/B ratio", "P/S ratio")
        )
        fig.add_trace(go.Bar(x=df['Symbol'],
                            y=df['pe_ratio']), 
                    1, 1)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['peg_ratio']), 
                    1, 2)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['eps_ratio']), 
                    1, 3)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['pb_ratio']), 
                    1, 4)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['ps_ratio']), 
                    1, 5)
        fig.update_layout(
            title_text=f"Financial Ratios",
            showlegend=False,
            height=600
        )
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_left_prices', 'children'),
              Input('company_vs_left_symbol', 'value'))
def show_vs_left_prices(symbol):
    """Figure of Left Company Price History on Company VS page"""
    try:
        company = yf.Ticker(symbol)
        df = company.history(period="10y")
        df = df.reset_index()
        if df.empty:
            return html.Div()
    except:
        return html.Div()
    else:
        fig = px.line(df, x='Date', y="Close", title=f'Historical Prices')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_left_emissions', 'children'),
              Input('company_vs_left_symbol', 'value'))
def emission_vs_left_vs_time(symbol):
    """Figure of Left Company Emission on Company VS page"""
    try:
        company_emission_data = pd.merge(
            left=facility_ghg_data,
            right=facility_company_year_data,
            on='Facility Gov ID')
        
        company_emission_data = company_emission_data.groupby(['Symbol','GHG Year'])[['co2', 'ch4', 'n2o']].apply(sum)
        company_emission_data.reset_index(inplace=True)
        l = symbol.split(',')
        df = company_emission_data.set_index('Symbol')
        df= df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(rows=1, cols=3, shared_xaxes=True, subplot_titles=("CO2", "CH4", "N2O"))
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['co2'], mode = 'lines+markers'), 1, 1)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['ch4'], mode = 'lines+markers'), 1, 2)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['n2o'], mode = 'lines+markers'), 1, 3)
        fig.update_layout(title_text=f"Company Emissions", showlegend=False, title_x=0.5)
        return dcc.Graph(figure=fig)
    

@app.callback(Output('company_vs_left_emission_map', 'children'),
              Input('company_vs_left_symbol', 'value'),
              Input('company_vs_gas', 'value'))
def draw_vs_left_emissions_map(symbol, gas):
    """Figure of Left Company Emission Map on Company VS page"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol', 
                        right_on='Symbol')
        data = pd.merge(left=data, 
                        right=facility_ghg_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.density_mapbox(data, 
                                lat='Latitude', 
                                lon='Longitude', 
                                z=gas, 
                                radius=50,
                                center=dict(lat=40, lon=270), 
                                zoom=2,
                                mapbox_style="stamen-terrain",
                                animation_frame="GHG Year")
        fig.update_layout(mapbox_style="open-street-map", title='Emissions')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_left_facilities_map', 'children'),
              Input('company_vs_left_symbol', 'value'))
def draw_vs_left_facilities_map(symbol) -> None:
    """Figure of Left Company Facilities Map on Company VS page"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol',
                        right_on='Symbol')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.scatter_mapbox(data,
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Industry", 
                                hover_data=["Address", "Zip Code"],
                                color="Industry",
                                center=dict(lat=40, lon=270),
                                color_discrete_sequence=px.colors.sequential.Turbo, 
                                zoom=2)
        fig.update_layout(mapbox_style="open-street-map", title='Faclities Map')
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Callbacks for the Right Company on Company VS Page
# --------------------------------------------------------
@app.callback(Output('company_vs_right_name', 'children'),
              Input('company_vs_right_symbol', 'value'))
def company_vs_right_name(symbol):
    """Name of Right Company on Company VS page"""
    try:
        symbol = symbol.upper()
        name = company_info_data[
            company_info_data['Symbol'] == symbol
        ].iloc[0,1]
    except:
        return 'No company found'
    else:  
        name = name.replace('Common Stock', '')
        name = name.replace('Shares', '')
        name = name.replace('Ordinary Shares', '')
        return name


@app.callback(Output('company_vs_right_esg', 'children'),
              Input('company_vs_right_symbol', 'value'))
def company_vs_right_esg(symbol):
    """Figure of Right Company ESG Scores on Company VS page"""
    try:
        l  = symbol.split(',')
        df = company_esg_scores_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        character = ['ESG Score', 
                    'Environment', 'Emissions', 'Resource Use', 'Innovation',
                    'Social', 'Human Rights', 'Product Responsibility', 'Workforce', 'Community',
                    'Governance', 'Management', 'Shareholders', 'CSR Strategy']
        parent = ['', 
                'ESG Score', 'Environment', 'Environment', 'Environment', 
                'ESG Score', 'Social', 'Social', 'Social', 'Social',
                'ESG Score', 'Governance', 'Governance', 'Governance']
        value = [df.iloc[0,2], 
                df.iloc[0,3], df.iloc[0,4], df.iloc[0,5], df.iloc[0,6],
                df.iloc[0,7], df.iloc[0,8], df.iloc[0,9], df.iloc[0,10], df.iloc[0,11],
                df.iloc[0,12], df.iloc[0,13], df.iloc[0,14], df.iloc[0,15]]
        labels = { character[i]: value[i] for i in range(len(character)) }
        data = {
            'character': character,
            'parent': parent,
            'value': value
        }
        fig = px.sunburst(
            data,
            names='character',
            values='value',
            parents='parent',
            title='ESG Breakdown',
            labels=labels,
            height=600
        )
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_right_ratios', 'children'),
              Input('company_vs_right_symbol', 'value'))
def show_vs_right_ratios(symbol):
    """Figure of Right Company Financial Ratios on Company VS page"""
    try:
        l = symbol.split(',')
        df = company_fin_info_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(
            rows=1, 
            cols=5, 
            shared_xaxes=True,
            subplot_titles=("P/E ratio", "PEG ratio", "EPS ratio", "P/B ratio", "P/S ratio")
        )
        fig.add_trace(go.Bar(x=df['Symbol'],
                            y=df['pe_ratio']), 
                    1, 1)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['peg_ratio']), 
                    1, 2)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['eps_ratio']), 
                    1, 3)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['pb_ratio']), 
                    1, 4)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['ps_ratio']), 
                    1, 5)
        fig.update_layout(
            title_text=f"Financial Ratios",
            showlegend=False,
            height=600
        )
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_right_prices', 'children'),
              Input('company_vs_right_symbol', 'value'))
def show_vs_right_prices(symbol):
    """Figure of Right Company Price History on Company VS page"""
    try:
        company = yf.Ticker(symbol)
        df = company.history(period="10y")
        df = df.reset_index()
        if df.empty:
            return html.Div()
    except:
        return html.Div()
    else:
        fig = px.line(df, x='Date', y="Close", title=f'Historical Prices')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_right_emissions', 'children'),
              Input('company_vs_right_symbol', 'value'))
def emission_vs_right_vs_time(symbol):
    """Figure of Right Company Emissions on Company VS page"""
    try:
        company_emission_data = pd.merge(
            left=facility_ghg_data,
            right=facility_company_year_data,
            on='Facility Gov ID')
        
        company_emission_data = company_emission_data.groupby(['Symbol','GHG Year'])[['co2', 'ch4', 'n2o']].apply(sum)
        company_emission_data.reset_index(inplace=True)
        l = symbol.split(',')
        df = company_emission_data.set_index('Symbol')
        df= df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(rows=1, cols=3, shared_xaxes=True, subplot_titles=("CO2", "CH4", "N2O"))
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['co2'], mode = 'lines+markers'), 1, 1)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['ch4'], mode = 'lines+markers'), 1, 2)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['n2o'], mode = 'lines+markers'), 1, 3)
        fig.update_layout(title_text=f"Company Emissions", showlegend=False, title_x=0.5)
        return dcc.Graph(figure=fig)
    

@app.callback(Output('company_vs_right_emission_map', 'children'),
              Input('company_vs_right_symbol', 'value'),
              Input('company_vs_gas', 'value'))
def draw_vs_right_emissions_map(symbol, gas):
    """Figure of Right Company Emissions Map on Company VS page"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol', 
                        right_on='Symbol')
        data = pd.merge(left=data, 
                        right=facility_ghg_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.density_mapbox(data, 
                                lat='Latitude', 
                                lon='Longitude', 
                                z=gas, 
                                radius=50,
                                center=dict(lat=40, lon=270), 
                                zoom=2,
                                mapbox_style="stamen-terrain",
                                animation_frame="GHG Year")
        fig.update_layout(mapbox_style="open-street-map", title='Emissions')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_vs_right_facilities_map', 'children'),
              Input('company_vs_right_symbol', 'value'))
def draw_vs_right_facilities_map(symbol) -> None:
    """Figure of Right Company Facilities Map on Company VS page"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol',
                        right_on='Symbol')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.scatter_mapbox(data,
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Industry", 
                                hover_data=["Address", "Zip Code"],
                                color="Industry",
                                center=dict(lat=40, lon=270),
                                color_discrete_sequence=px.colors.sequential.Turbo, 
                                zoom=2)
        fig.update_layout(mapbox_style="open-street-map", title='Faclities Map')
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Single Company Page Layout
# --------------------------------------------------------
def company_view():
    return html.Div([
        # Left Column: Menu
        html.Div([
            html.Div([
                # Ticker Picker
                html.H6('Symbol: '),
                dcc.Input(id='company_symbol',
                          type='text',
                          value='TSLA'),
                html.P("^ enter company's ticker", style={'color': 'grey'}),
                
                # Gas Picker
                html.H6('Gas: '),
                dcc.Dropdown(
                    id='company_gas',
                    options=[
                        {'label': 'Carbon Dioxide (CO2)', 'value': 'co2'},
                        {'label': 'Methane (CH4)', 'value': 'ch4'},
                        {'label': 'Nitrous (N2O)', 'value': 'n2o'}
                    ],
                    value='co2'
                ),
            ]),
        ], className="two columns"),
        
        # Right Column: Figures
        html.Div([
            # Company Name and Description, Row 1
            html.Div([ 
                html.Div([ 
                    # Top: Name
                    html.H3(id='company_name'),
                    # Bottom: Description
                    html.P(id='company_description', style={'color': '#808080'}),
                ], className="twelve columns")
            ], className="row"),
            
            # Company Visuals, Row 2
            html.Div([
                # Left: ESG Figure
                html.Div(id='company_esg', className='six columns'),
                # Right: Ratios Figure
                html.Div(id='company_ratios', className='six columns')
            ], className="row"),
            
            # Company Visuals, Row 3
            html.Div([
                # Full Width: Prices
                html.Div(id='company_prices', className="twelve columns"),
            ], className="row"),
            
            # Company Visuals, Row 4
            html.Div([
                # Emissions
                html.Div(id='company_emissions', className="twelve columns"),
            ], className="row"),
            
            # Company Visuals, Row 5, Maps
            html.Div([
                # Emissions
                html.Div(id='company_emission_map', className="six columns"),
                html.Div(id='company_facilities_map', className="six columns"),
            ], className="row"),
        ], className="ten columns")
    ], className="row")


# --------------------------------------------------------
# Callbacks for Single Company Page
# --------------------------------------------------------
@app.callback(Output('company_name', 'children'),
              Input('company_symbol', 'value'))
def company_name(symbol):
    """Company Name for Single Company View"""
    try:
        symbol = symbol.upper()
        name = company_info_data[
            company_info_data['Symbol'] == symbol
        ].iloc[0,1]
    except:
        return 'No company found'
    else:  
        name = name.replace('Common Stock', '')
        name = name.replace('Shares', '')
        name = name.replace('Ordinary Shares', '')
        return name


@app.callback(Output('company_description', 'children'),
              Input('company_symbol', 'value'))
def company_description(symbol):
    """Company Description for Single Company View"""
    try:
        symbol = symbol.upper()
        description = company_description_data[
            company_description_data['Symbol'] == symbol
        ].iloc[0,1]
    except:
        description = ''
    
    return description


@app.callback(Output('company_esg', 'children'),
              Input('company_symbol', 'value'))
def company_esg(symbol):
    """Figure of Company ESG Scores for Single Company View"""
    try:
        l  = symbol.split(',')
        df = company_esg_scores_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        character = ['ESG Score', 
                    'Environment', 'Emissions', 'Resource Use', 'Innovation',
                    'Social', 'Human Rights', 'Product Responsibility', 'Workforce', 'Community',
                    'Governance', 'Management', 'Shareholders', 'CSR Strategy']
        parent = ['', 
                'ESG Score', 'Environment', 'Environment', 'Environment', 
                'ESG Score', 'Social', 'Social', 'Social', 'Social',
                'ESG Score', 'Governance', 'Governance', 'Governance']
        value = [df.iloc[0,2], 
                df.iloc[0,3], df.iloc[0,4], df.iloc[0,5], df.iloc[0,6],
                df.iloc[0,7], df.iloc[0,8], df.iloc[0,9], df.iloc[0,10], df.iloc[0,11],
                df.iloc[0,12], df.iloc[0,13], df.iloc[0,14], df.iloc[0,15]]
        labels = { character[i]: value[i] for i in range(len(character)) }
        data = {
            'character': character,
            'parent': parent,
            'value': value
        }
        fig = px.sunburst(
            data,
            names='character',
            values='value',
            parents='parent',
            title='ESG Breakdown',
            labels=labels,
            height=600
        )
        return dcc.Graph(figure=fig)


@app.callback(Output('company_ratios', 'children'),
              Input('company_symbol', 'value'))
def show_ratios(symbol):
    """Figure of Company Financial Ratios for Single Company View"""
    try:
        l = symbol.split(',')
        df = company_fin_info_data.set_index('Symbol')
        df = df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(
            rows=1, 
            cols=5, 
            shared_xaxes=True,
            subplot_titles=("P/E ratio", "PEG ratio", "EPS ratio", "P/B ratio", "P/S ratio")
        )
        fig.add_trace(go.Bar(x=df['Symbol'],
                            y=df['pe_ratio']), 
                    1, 1)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['peg_ratio']), 
                    1, 2)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['eps_ratio']), 
                    1, 3)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['pb_ratio']), 
                    1, 4)
        fig.add_trace(go.Bar(x=df['Symbol'], 
                            y=df['ps_ratio']), 
                    1, 5)
        fig.update_layout(
            title_text=f"Financial Ratios",
            showlegend=False,
            height=600
        )
        return dcc.Graph(figure=fig)


@app.callback(Output('company_prices', 'children'),
              Input('company_symbol', 'value'))
def show_prices(symbol):
    """Figure of Company Price History for Single Company View"""
    try:
        company = yf.Ticker(symbol)
        df = company.history(period="10y")
        df = df.reset_index()
        if df.empty:
            return html.Div()
    except:
        return html.Div()
    else:
        fig = px.line(df, x='Date', y="Close", title=f'Historical Prices')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_emissions', 'children'),
              Input('company_symbol', 'value'))
def emission_vs_time(symbol):
    """Figure of Company Emissions for Single Company View"""
    try:
        company_emission_data = pd.merge(
            left=facility_ghg_data,
            right=facility_company_year_data,
            on='Facility Gov ID')
        company_emission_data = company_emission_data.groupby(['Symbol','GHG Year'])[['co2', 'ch4', 'n2o']].apply(sum)
        company_emission_data.reset_index(inplace=True)
        l = symbol.split(',')
        df = company_emission_data.set_index('Symbol')
        df= df.loc[l]
        df = df.reset_index()
    except:
        return html.Div()
    else:
        fig = make_subplots(rows=1, cols=3, shared_xaxes=True, subplot_titles=("CO2", "CH4", "N2O"))
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['co2'], mode = 'lines+markers'), 1, 1)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['ch4'], mode = 'lines+markers'), 1, 2)
        fig.add_trace(go.Scatter(x=df['GHG Year'], y=df['n2o'], mode = 'lines+markers'), 1, 3)
        fig.update_layout(title_text=f"Company Emissions", showlegend=False, title_x=0.5)
        return dcc.Graph(figure=fig)
    

@app.callback(Output('company_emission_map', 'children'),
              Input('company_symbol', 'value'),
              Input('company_gas', 'value'))
def draw_emissions_map(symbol, gas):
    """Figure of Company Emissions Map for Single Company View"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol', 
                        right_on='Symbol')
        data = pd.merge(left=data, 
                        right=facility_ghg_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.density_mapbox(data, 
                                lat='Latitude', 
                                lon='Longitude', 
                                z=gas, 
                                radius=50,
                                center=dict(lat=40, lon=270), 
                                zoom=2,
                                mapbox_style="stamen-terrain",
                                animation_frame="GHG Year")
        fig.update_layout(mapbox_style="open-street-map", title='Emissions')
        return dcc.Graph(figure=fig)


@app.callback(Output('company_facilities_map', 'children'),
              Input('company_symbol', 'value'))
def draw_facilities_map(symbol) -> None:
    """Figure of Company Facilities Map for Single Company View"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol',
                        right_on='Symbol')
        data = data.loc[data['Symbol'] == symbol]
    except:
        return html.Div()
    else:
        fig = px.scatter_mapbox(data,
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Industry", 
                                hover_data=["Address", "Zip Code"],
                                color="Industry",
                                center=dict(lat=40, lon=270),
                                color_discrete_sequence=px.colors.sequential.Turbo, 
                                zoom=2)
        fig.update_layout(mapbox_style="open-street-map", title='Faclities Map')
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Industry Page Layout
# --------------------------------------------------------
def industry_view():
    return html.Div([
        # Left Column: Menu
        html.Div([
            html.Div([
                # Ticker Picker
                html.H6('Industry: '),
                dcc.Dropdown(
                    id='industry_name',
                    options=industry_options,
                    value='All'
                ),
                
                html.H6('Gas: '),
                dcc.Dropdown(
                    id='industry_gas',
                    options=[
                        {'label': 'Carbon Dioxide (CO2)', 'value': 'co2'},
                        {'label': 'Methane (CH4)', 'value': 'ch4'},
                        {'label': 'Nitrous (N2O)', 'value': 'n2o'}
                    ],
                    value='co2'
                ),
            ]),
        ], className="two columns"),
        
        # Right Column: Figures
        html.Div([
            # Industry Visuals, Row 1
            html.Div([
                html.Div(id='industry_emission_map', className='twelve columns'),
                html.Div(id='industry_facilities_map', className='twelve columns'),
            ], className="row"),
        ], className="ten columns")
    ], className="row")

    
# --------------------------------------------------------
# Callbacks for Industry Page
# --------------------------------------------------------
@app.callback(Output('industry_emission_map', 'children'),
              Input('industry_name', 'value'),
              Input('industry_gas', 'value'))
def draw_emissions_map(industry, gas):
    """Emissions Map by Industry Figure"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol', 
                        right_on='Symbol')
        data = pd.merge(left=data, 
                        right=facility_ghg_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        if not industry == 'All':
            data = data.loc[data['Industry'] == industry]
    except:
        return html.Div()
    else:
        fig = px.density_mapbox(data, 
                                lat='Latitude', 
                                lon='Longitude', 
                                z=gas, 
                                radius=50,
                                center=dict(lat=40, lon=270), 
                                zoom=3,
                                mapbox_style="stamen-terrain",
                                animation_frame="GHG Year")
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(height=1000, title='Emission by Year Across Industries')
        return dcc.Graph(figure=fig)


@app.callback(Output('industry_facilities_map', 'children'),
              Input('industry_name', 'value'))
def draw_facilities_map(industry) -> None:
    """Facilities Map by Industry Figure"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol',
                        right_on='Symbol')
        if not industry == 'All':
            data = data.loc[data['Industry'] == industry]
    except:
        return html.Div()
    else:
        fig = px.scatter_mapbox(data,
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Company Name", 
                                hover_data=["Address", "Zip Code"],
                                color="Industry",
                                color_discrete_sequence=px.colors.sequential.Turbo, 
                                zoom=3, 
                                center=dict(lat=40, lon=270),
                                height=1000)
        fig.update_layout(mapbox_style="open-street-map", title='Faclities Map by Industries')
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Sector Page Layout
# --------------------------------------------------------
def sector_view():
    """View for the Sector Page"""
    return html.Div([
        # Left Column: Menu
        html.Div([
            html.Div([
                # Ticker Picker
                html.H6('Sector: '),
                dcc.Dropdown(
                    id='sector_name',
                    options=sector_options,
                    value='All'
                ),
                
                html.H6('Gas: '),
                dcc.Dropdown(
                    id='sector_gas',
                    options=[
                        {'label': 'Carbon Dioxide (CO2)', 'value': 'co2'},
                        {'label': 'Methane (CH4)', 'value': 'ch4'},
                        {'label': 'Nitrous (N2O)', 'value': 'n2o'}
                    ],
                    value='co2'
                ),
            ]),
        ], className="two columns"),
        
        # Right Column: Figures
        html.Div([
            # Industry Visuals, Row 1
            html.Div([
                html.Div(id='sector_emission_map', className='twelve columns'),
                html.Div(id='sector_facilities_map', className='twelve columns'),
            ], className="row"),
        ], className="ten columns")
    ], className="row")


# --------------------------------------------------------
# Callbacks for Sector Page
# --------------------------------------------------------
@app.callback(Output('sector_emission_map', 'children'),
              Input('sector_name', 'value'),
              Input('sector_gas', 'value'))
def draw_emissions_map(sector, gas):
    """Emissions Map by Sector Figure"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol', 
                        right_on='Symbol')
        data = pd.merge(left=data, 
                        right=facility_ghg_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        if not sector == 'All':
            data = data.loc[data['Sector'] == sector]
    except:
        return html.Div()
    else:
        fig = px.density_mapbox(data, 
                                lat='Latitude', 
                                lon='Longitude', 
                                z=gas, 
                                radius=50,
                                center=dict(lat=40, lon=270), 
                                zoom=3,
                                mapbox_style="stamen-terrain",
                                animation_frame="GHG Year")
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(height=1000, title='Emission by Year Across Sectors')
        return dcc.Graph(figure=fig)


@app.callback(Output('sector_facilities_map', 'children'),
              Input('sector_name', 'value'))
def draw_facilities_map(sector) -> None:
    """Facilities Map by Sector Figure"""
    try:
        data = pd.merge(left=facility_info_data, 
                        right=facility_company_year_data, 
                        left_on='Facility Gov ID', 
                        right_on='Facility Gov ID')
        data = pd.merge(left=data,
                        right=company_info_data, 
                        left_on='Symbol',
                        right_on='Symbol')
        if not sector == 'All':
            data = data.loc[data['Sector'] == sector]
    except:
        return html.Div()
    else:
        fig = px.scatter_mapbox(data,
                                lat="Latitude", 
                                lon="Longitude", 
                                hover_name="Company Name", 
                                hover_data=["Address", "Zip Code"],
                                color="Sector",
                                center=dict(lat=40, lon=270),
                                color_discrete_sequence=px.colors.sequential.Turbo, 
                                zoom=3, 
                                height=1000)
        fig.update_layout(mapbox_style="open-street-map", 
                          title='Faclities Map by Sector')
        return dcc.Graph(figure=fig)


# --------------------------------------------------------
# Tab Controller
# --------------------------------------------------------
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    """Controller for the tab menu, 
       based on the chosen tab displays correct view"""
    if tab == 'main-tab':
        return main_view()
    elif tab == 'company-tab':
        return company_view()
    elif tab == 'company-vs-tab':
        return company_vs_view()
    elif tab == 'industry-tab':
        return industry_view()
    elif tab == 'sector-tab':
        return sector_view()


# --------------------------------------------------------
# Run App
# --------------------------------------------------------
if __name__ == '__main__':
    port = os.environ.get['PORT', 8050]
    app.run_server(debug=True, port=port)