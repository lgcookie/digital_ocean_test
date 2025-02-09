from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import os
import dash

def register_callbacks(app):
    @app.callback(
        Output("dummy", "data"),  # Dummy output to trigger clientside callback
        [Input("delete-simulation", "n_clicks")],
        [State("file-selector", "value")]
    )
    def delete_simulation(n_clicks, selected_file):
        if n_clicks is None or selected_file is None:
            raise PreventUpdate
            
        # Don't allow deletion of example simulation
        if selected_file == "Simulation Example_20250209_114855.csv":
            return selected_file, dash.no_update
            
        try:
            # Delete the CSV file
            csv_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", selected_file)
            if os.path.exists(csv_path):
                os.remove(csv_path)
                
            # Delete the corresponding params file
            base_name = selected_file.rsplit('.', 1)[0]
            params_file = f"{base_name}_params.json"
            params_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", params_file)
            if os.path.exists(params_path):
                os.remove(params_path)
            
            # Return trigger for page refresh
            return True
            
        except Exception as e:
            print(f"Error deleting files: {e}")
            return dash.no_update

    # Add clientside callback to refresh the page
    app.clientside_callback(
        """
        function(trigger) {
            if(trigger) {
                window.location.reload();
                return null;
            }
            return null;
        }
        """,
        Output("dummy", "data", allow_duplicate=True),
        Input("dummy", "data"),
        prevent_initial_call=True
    )