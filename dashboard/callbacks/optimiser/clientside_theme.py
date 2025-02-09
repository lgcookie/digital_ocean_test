from dash.dependencies import Input, Output, State
import dash
from dash.dependencies import Input, Output, State
import dash

def register_callbacks(app):
    @app.callback(
        [Output("color-scheme", "children"),
         Output("selected-colors", "data"),
         Output("optimisation", "data-theme")],  # Add data-theme output
        Input("color-switch", "on")
    )
    def update_color_scheme(dark_mode):
        if dark_mode:
            colors = {
                'background': '#1A1B1E',
                'text': '#FFFFFF',
                'graph_line_primary': '#FFFFFF',
                'graph_line_secondary': '#ff8400',
                'graph_line_tertiary': '#9cd404',
                'plot-background': 'rgba(26,27,30,0.8)',
                'paper-background': 'rgba(26,27,30,0)',
                'grid-color': '#2C2E33',
                'axis-color': '#FFFFFF',
                'header-text': '#FFFFFF',
                'mini-container': '#2C2E33',  # Darker shade for containers in dark mode
                'container': '#1A1B1E',
                'background-primary': '#1A1B1E',
                'background-secondary': '#2C2E33',
                'text-primary': '#FFFFFF',
                'hover-background': '#2C2E33',
                'border-color': '#2C2E33',
                'dropdown-background': '#1A1B1E',
                'dropdown-text': '#FFFFFF',
                'input-background': '#2C2E33',
                'input-text': '#FFFFFF'
            }
            return "Dark", colors, "dark"
        else:
            colors = {
                'background': '#FFFFFF',
                'text': '#2E2E2E',
                'graph_line_primary': '#2E2E2E',
                'graph_line_secondary': '#ff8400',
                'graph_line_tertiary': '#9cd404',
                'plot-background': 'rgba(255,255,255,0.8)',
                'paper-background': 'rgba(255,255,255,0)',
                'grid-color': '#E9ECEF',
                'axis-color': '#2E2E2E',
                'header-text': '#2E2E2E',
                'mini-container': '#FFFFFF',  # Light background for containers in light mode
                'container': '#F8F9FA',
                'background-primary': '#FFFFFF',
                'background-secondary': '#E9ECEF',
                'text-primary': '#2E2E2E',
                'hover-background': '#F8F9FA',
                'border-color': '#E9ECEF',
                'dropdown-background': '#FFFFFF',
                'dropdown-text': '#2E2E2E',
                'input-background': '#FFFFFF',
                'input-text': '#2E2E2E'
            }
            return "Light", colors, "light"