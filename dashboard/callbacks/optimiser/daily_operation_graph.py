from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import orjson
import plotly.graph_objects as go

def register_callbacks(app):
    @app.callback(
    [Output("daily-operation-graph", "figure")],
    [Input("optimisation-result", "data"),
     Input("graph-layout", "data"),
     Input("selected-colors", "data"),
     Input("date-selector", "date")],
    )
    def plot_daily_operation(optimiser_dict, layout, selected_colors, date):
        if optimiser_dict is None or date is None:
            raise PreventUpdate
     
        # Convert back to DataFrame with datetime index
        optimiser_df = pd.DataFrame(optimiser_dict)
        optimiser_df['time'] = pd.to_datetime(optimiser_df['time'])
        optimiser_df.set_index('time', inplace=True)
        date = pd.to_datetime(date).date()
        
        mask = (optimiser_df.index.date == date)
        optimiser_selected_df = optimiser_df[mask]
        if optimiser_selected_df.empty:
            raise PreventUpdate

        datas = []
        
        # Get colors from selected_colors with fallbacks
        primary_color = selected_colors.get("graph_line_primary", "#000000")
        secondary_color = selected_colors.get("graph_line_secondary", "#d40434")
        
        # Add Day Ahead Export
        datas.append(
            dict(
                type="bar",
                name="Day Ahead",
                x=optimiser_selected_df.index,
                y=optimiser_selected_df['export_da_vol'],
                marker=dict(color=secondary_color),
                hovertemplate=
                '<br><b>Day Ahead Export</b>'+
                '<br><b>Power: %{y:.2f} MW</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )
        
        # Add Day Ahead Import (negative values)
        datas.append(
            dict(
                type="bar",
                name="Day Ahead Import",
                showlegend=False,
                x=optimiser_selected_df.index,
                y=-optimiser_selected_df['import_da_vol'],
                marker=dict(color=secondary_color),
                hovertemplate=
                '<br><b>Day Ahead Import</b>'+
                '<br><b>Power: %{y:.2f} MW</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )
        # Add Day Ahead Export
        datas.append(
            dict(
                type="bar",
                name="Intraday",
                x=optimiser_selected_df.index,
                y=optimiser_selected_df['export_intraday_vol'],
                marker=dict(color=primary_color),
                hovertemplate=
                '<br><b>Intraday Export</b>'+
                '<br><b>Power: %{y:.2f} MW</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )
        
        # Add Day Ahead Import (negative values)
        datas.append(
            dict(
                type="bar",
                name="Intraday Import",
                showlegend=False,
                x=optimiser_selected_df.index,
                y=-optimiser_selected_df['import_intraday_vol'],
                marker=dict(color=primary_color),
                hovertemplate=
                '<br><b>Intraday Import</b>'+
                '<br><b>Power: %{y:.2f} MW</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )
        # Add Intraday Export
        datas.append(
            dict(
                type="scatter",
                name="Day Ahead Price",
                x=optimiser_selected_df.index,
                y=optimiser_selected_df['day_ahead_price'],
                yaxis="y2",
                line=dict(
                    color=secondary_color,
                    dash='dash'
                ),
                hovertemplate=
                '<br><b>Day Ahead Price</b>'+
                '<br><b>Price: £%{y:.2f}/MWh</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )

        # Add Intraday Price line
        datas.append(
            dict(
                type="scatter",
                name="Intraday Price",
                x=optimiser_selected_df.index,
                y=optimiser_selected_df['intraday_price'],
                yaxis="y2",
                line=dict(
                    color=primary_color,
                    dash='dash'
                ),
                hovertemplate=
                '<br><b>Intraday Price</b>'+
                '<br><b>Price: £%{y:.2f}/MWh</b>'+
                '<br><b>Time: %{x}</b>'+
                '<extra></extra>',
            )
        )

        layout = orjson.loads(layout) if isinstance(layout, str) else layout
        layout["title"] = dict(
        text=f"Daily Operation - {date}",
        x=0.5,
        y=0.95,
        xanchor="center",
        yanchor="top",
        font=dict(
            color=selected_colors.get("header-text", "#000000"),
            size=18
        )
    )
        layout["barmode"] = "stack"
        
        layout["yaxis"] = dict(
            title=dict(
                text="Power (MW)",
                font=dict(
                    color=selected_colors.get("header-text", "#000000"),
                    size=16
                ),
                standoff=15
            ),
            showline=True,
            linewidth=2,
            linecolor=selected_colors.get("header-text", "#000000"),
            showgrid=False
        )
        layout["yaxis2"] = dict(
            title=dict(
                text="Price (£/MWh)",
                font=dict(
                    color=selected_colors.get("header-text", "#000000"),
                    size=16
                ),
                standoff=15
            ),
            showline=True,
            linewidth=2,
            linecolor=selected_colors.get("header-text", "#000000"),
            showgrid=False,
            side="right",
            overlaying='y'
        )
        layout["xaxis"] = dict(
            title=dict(
                text="Date",
                font=dict(
                    color=selected_colors.get("header-text", "#000000"),
                    size=16
                ),
                standoff=15
            ),
            showline=True,
            linewidth=2,
            linecolor=selected_colors.get("header-text", "#000000"),
            showgrid=False
        )
        
        

        figure = dict(data=datas, layout=layout)
        return [figure]