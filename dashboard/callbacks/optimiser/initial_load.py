
from dash.dependencies import Input, Output, State
import json

from dash.exceptions import PreventUpdate
def register_callbacks(app):

    @app.callback(
    [
    Output("graph-layout", "data"),
    ],
    [
    Input("selected-colors", "data"),
    ]

    )
    def graph_layout(colors):
        colors = colors
        
        layout = dict(
        autosize=True,
        automargin=True,
        hovermode="closest",
        plot_bgcolor=colors["plot-background"],
        paper_bgcolor=colors["plot-background"],
        legend=dict(font=dict(size=14), orientation="h"),
        hoverlabel = dict(bgcolor=colors["plot-background"]),
        font=dict(color=colors["header-text"],size=18),
        xaxis=dict(showline=True,linewidth=2,linecolor=colors["header-text"],showgrid=False),
        yaxis=dict(showline=True,linewidth=2,linecolor=colors["header-text"],showgrid=False),
        mapbox=dict(
            style="light",
            center=dict(lon=-78.05, lat=42.54),
            zoom=7,
            bgcolor=colors["plot-background"]
        ),
        geo=dict(bgcolor=colors["plot-background"]),
        
        title_font=dict(
            title_font_color=colors["header-text"]
        )
        )
        return [json.dumps(layout)]