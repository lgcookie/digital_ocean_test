from dash.dependencies import Input, Output
from dash import dcc
from dash import html
# Import required libraries
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_mantine_components as dmc
import dash_loading_spinners as dls
from dash import dcc, html
import pandas as pd
from dashboard.styles import colors
from dash import html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_loading_spinners as dls
import dash

layout = html.Div(
    id="optimisation",
    className="page-container",
    children=[
        # Loading Screen
        html.Div(
            id="loading-screen",
            style={"display": "none"},
            children=[
                html.H1("Generating optimisation Overview"),
                dbc.Spinner(
                    type="border", 
                    color="warning", 
                    fullscreen=False, 
                    spinner_style={
                        "width": "10rem", 
                        "height": "10rem",
                        "margin-top": "5rem"
                    }
                )
            ]
        ),
        
        # Main Content
        html.Div(
            id="main-content",
            style={
                "display": "flex",
                "height": "calc(100vh - 70px)",  # Subtract header height
                "overflow": "hidden"
            },
            children=[
                # Sidebar
                html.Div(
                    className="sidebar-container",
                    children=[
                        html.H4("Simulation Parameters"),
                        html.Div([
                            html.Label("Simulation Name:", className="input_label"),
                            dcc.Input(
                                id="simulation-name",
                                type="text",
                                value="Simulation Name",
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Battery Power (MW):", className="input_label"),
                            dcc.Input(
                                id="battery-power",
                                type="number",
                                value=100,
                                min=0,
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Energy Capacity (MWh):", className="input_label"),
                            dcc.Input(
                                id="energy-capacity",
                                type="number",
                                value=100,
                                min=0,
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Charging Efficiency (%):", className="input_label"),
                            dcc.Input(
                                id="charging-efficiency",
                                type="number",
                                value=85,
                                min=0,
                                max=100,
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Discharging Efficiency (%):", className="input_label"),
                            dcc.Input(
                                id="discharging-efficiency",
                                type="number",
                                value=85,
                                min=0,
                                max=100,
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Max Daily Cycles:", className="input_label"),
                            dcc.Input(
                                id="max-daily-cycles",
                                type="number",
                                value=2,
                                min=0,
                                className="input_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Label("Price Timeseries:", className="input_label"),
                            dcc.Dropdown(
                                id="price-timeseries",
                                options=[{"label": "Default", "value": "default"},{"label": "10% Higher Volatility", "value": "default"}]],
                                value="default",
                                className="dropdown_field",
                                style={"width": "100%"}
                            ),
                            
                            html.Button(
                                "Run Simulation",
                                id="run-simulation",
                                className="button-primary",
                                style={"width": "100%", "marginTop": "20px"}
                            )
                        ])
                    ]
                ),
                
                # Main Content Area
                html.Div(
                    className="main-content-container",
                    children=[
                        # File Selector and Delete Button
                        html.Div(
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "margin-bottom": "20px",
                                "padding": "15px",
                                "border-radius": "5px"
                            },
                            children=[
                                html.Label("Select Simulation:", style={"marginRight": "10px"}),
                                dcc.Dropdown(
                                    id="file-selector",
                                    value="Simulation Example_20250209_114855.csv",
                                    style={"flex": "1", "marginRight": "10px"}
                                ),
                                html.Button(
                                    "Delete Simulation",
                                    id="delete-simulation",
                                    className="button-primary"
                                )
                            ]
                        ),
                        
                        # Revenue Graph
                        html.Div(
                            style={
                                "padding": "15px",
                                "margin-bottom": "20px",
                                "border-radius": "5px"
                            },
                            children=[
                                html.H4(
                                id="revenue-graph-title", 
                                style={"color": "var(--text-primary)"}  # CSS variable will update this
                            ),
                                dls.TailSpin(
                                    dcc.Graph(id="total-revenue-graph"),
                                    color="#ff8400d9"
                                ),
                                
                            ]
                        ),
                        
                        # Daily Operation Graph
                        html.Div(
                            style={
                                "padding": "15px",
                                "border-radius": "5px"
                            },
                            children=[
                                
                                html.H4("Daily Operation"),
                                dcc.DatePickerSingle(
                                                    id='date-selector',
                                                    min_date_allowed=pd.to_datetime("2023-01-14"),
                                                    max_date_allowed=pd.to_datetime("2023-04-29"),
                                                    date=pd.to_datetime("2023-01-14"),
                                                    placeholder='Select a date',
                                                        ),
                                dls.TailSpin(
                                    dcc.Graph(id="daily-operation-graph"),
                                    color="#ff8400d9"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)