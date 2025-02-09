
from dashboard.callbacks.optimiser.optimisation import register_callbacks as optimisation_register_callbacks
from dashboard.callbacks.optimiser.revenue_graph import register_callbacks as revenue_graph_register_callbacks
from dashboard.callbacks.optimiser.load_data import register_callbacks as load_data_register_callbacks
from dashboard.callbacks.optimiser.initial_load import register_callbacks as initial_load_register_callbacks
from dashboard.callbacks.optimiser.file_selector import register_callbacks as file_selector_register_callbacks
from dashboard.callbacks.optimiser.daily_operation_graph import register_callbacks as daily_operation_graph_register_callbacks
from dashboard.callbacks.optimiser.revenue_graph_title import register_callbacks as revenue_graph_title_register_callbacks
from dashboard.callbacks.optimiser.delete_simulation import register_callbacks as delete_simulation_register_callbacks
from dashboard.callbacks.optimiser.clientside_theme import register_callbacks as clientside_theme_register_callbacks

def register_callbacks(app):
   
    initial_load_register_callbacks(app)
    optimisation_register_callbacks(app)
    revenue_graph_register_callbacks(app)
    load_data_register_callbacks(app)
    file_selector_register_callbacks(app)
    delete_simulation_register_callbacks(app)
    revenue_graph_title_register_callbacks(app)
    clientside_theme_register_callbacks(app)  # Add this line
    daily_operation_graph_register_callbacks(app)

    
