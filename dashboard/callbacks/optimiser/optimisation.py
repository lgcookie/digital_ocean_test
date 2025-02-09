from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import os
import json

from optimisation.main import run_optimisation
from optimisation.config.setup import Config
from datetime import datetime
def register_callbacks(app):
    @app.callback(
        Input("run-simulation", "n_clicks"),
        [State("simulation-name", "value"),
         State("battery-power", "value"),
         State("energy-capacity", "value"),
         State("charging-efficiency", "value"),
         State("discharging-efficiency", "value"),
         State("max-daily-cycles", "value"),
         State("price-timeseries", "value")]
    )
    def handle_simulation(n_clicks, sim_name, power, capacity, charging_eff, discharging_eff, daily_cycles, price_file):
        if n_clicks is None:
            raise PreventUpdate
            
        # Create config with user parameters
        config = Config()
        config.power = power
        config.capacity = capacity
        config.charging_efficiency = charging_eff / 100  # Convert from percentage
        config.discharging_efficiency = discharging_eff / 100
        config.daily_cycles = daily_cycles
            # Generate filename with simulation name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not sim_name:
            sim_name = "simulation"
        filename = f"{sim_name}_{timestamp}.csv"
        
            # Save parameters as metadata in a separate JSON file
        params = {
            "simulation_name": sim_name,
            "power_capacity": power,
            "energy_capacity": capacity,
            "charging_efficiency": charging_eff,
            "discharging_efficiency": discharging_eff,
            "max_daily_cycles": daily_cycles,
            "price_file": price_file,
            "timestamp": timestamp
        }
        
        params_filename = f"{sim_name}_{timestamp}_params.json"
        params_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", params_filename)
        
        with open(params_path, 'w') as f:
            json.dump(params, f)  # Changed from json.dumps to json.dump
        
        # Set output path in config
        config.output_path = os.path.join(os.getcwd(), "optimisation", "data_output", "raw_output", filename)
        # Run simulation
        run_optimisation(config)
      
            # Run simulation
        
        
        pass