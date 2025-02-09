from dash.dependencies import Input, Output
import pandas as pd
import os

def register_callbacks(app):
    @app.callback(
        Output('optimisation-result', 'data'),
        Input('file-selector', 'value')
    )
    def load_initial_data(selected_file):
        if selected_file is None:
            selected_file = "example_02-07.csv"
            
        # Load data from the selected file
        file_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", selected_file)
        optimiser_df = pd.read_csv(file_path, index_col=0).reset_index().rename(columns={'index': 'time'})
    
        return optimiser_df.to_dict('records')