from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import dash
def register_callbacks(app):
    @app.callback(
    Output('file-selector', 'options'),
    Input('file-selector', 'search_value')
    )
    def update_file_options(search_value):
        output_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output")
        files = [f for f in os.listdir(output_path) if f.endswith('.csv')]
        
        # Ensure example file is first in the list if it exists
        if "example_02-07.csv" in files:
            files.remove("example_02-07.csv")
            files.insert(0, "example_02-07.csv")
        
        # Create nice labels for the files
        options = []
        
        for f in files:
            if f == "example_02-07.csv":
                label = "Example Simulation"
            else:
                # Split filename into name and timestamp
                name_parts = f.replace('.csv', '').split('_')
                if len(name_parts) > 2:
                    sim_name = '_'.join(name_parts[:-2])  # Everything before the timestamp
                    timestamp = '_'.join(name_parts[-2:])  # The timestamp
                    label = f"{sim_name} ({timestamp})"
                else:
                    label = f
                    
            options.append({'label': label, 'value': f})
        
        return options
