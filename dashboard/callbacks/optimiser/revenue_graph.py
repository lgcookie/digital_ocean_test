from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import orjson

def register_callbacks(app):
    @app.callback(
    [Output("total-revenue-graph", "figure")],
    [Input("optimisation-result", "data"),
     Input("graph-layout", "data"),
     Input("selected-colors", "data")],
    )
    def plot_revenue(optimiser_dict, layout, selected_colors):
        if optimiser_dict is None:
            raise PreventUpdate
        
        # Convert back to DataFrame with datetime index
        optimiser_df = pd.DataFrame(optimiser_dict)
        optimiser_df['time'] = pd.to_datetime(optimiser_df['time'])  # Convert string to datetime
        optimiser_df.set_index('time', inplace=True)  # Set as index
        optimiser_revenue_df = optimiser_df[['cash_flow_bess_da', 'cash_flow_bess_intraday']]
        optimiser_revenue_daily_df = optimiser_revenue_df.groupby(optimiser_df.index.date).agg({
            'cash_flow_bess_da': 'sum', 
            'cash_flow_bess_intraday': 'sum'
        })

        datas = []
        # Get colors from the selected colors, with fallbacks
        primary_color = selected_colors.get("graph_line_primary", "#000000")
        secondary_color = selected_colors.get("graph_line_secondary", "#d40434")
        
        color_map = {
            'cash_flow_bess_da': primary_color,
            'cash_flow_bess_intraday': secondary_color
        }
        
        name_map = {
            'cash_flow_bess_da': "Day Ahead",
            'cash_flow_bess_intraday': "Intraday"
        }

        for service in optimiser_revenue_daily_df.columns:
            data = dict(
                type="bar",
                name=name_map[service],  # Use the friendly name from name_map
                x=optimiser_revenue_daily_df.index,
                y=optimiser_revenue_daily_df.loc[:,service],
                barmode="group",
                marker=dict(color=color_map[service]),
                hovertemplate=
                f'<br><b>{name_map[service]}</b>'+
                '<br><b>Revenue: £%{y:,.0f}</b>'+
                '<br><b>Date: %{x}</b>'+
                '<extra></extra>',
            )
            datas.append(data)
        
        layout = orjson.loads(layout) if isinstance(layout, str) else layout
        
        layout["barmode"] = "relative"
        
        layout["yaxis"] = dict(
            title=dict(
                text="Revenue (£)",
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
            side="left"
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