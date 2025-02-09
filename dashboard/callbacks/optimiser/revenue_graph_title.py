from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json
import os
def register_callbacks(app):
    @app.callback(
        [
        Output("revenue-graph-title", "children"),
        ],
        [Input("file-selector", "value")]
    )
    def update_parameter_displays(selected_file):
        if selected_file is None:
            return ["No file selected"] 
            
        # Get the corresponding parameters file
        base_name = selected_file.rsplit('.', 1)[0]
        params_file = f"{base_name}_params.json"
        params_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", params_file)
        
        try:
            with open(params_path, 'r') as f:
                params = json.load(f)
            title = f"{params['simulation_name']} - {params['power_capacity']} MW - {params['energy_capacity']} MWh - {params['charging_efficiency']}% - {params['discharging_efficiency']}%"
            print("this is the title",title)
            return [
                title
            ]
        except FileNotFoundError:
            return ["N/A"]