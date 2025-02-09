

from flask import Flask
from flask.helpers import get_root_path 
from dashboard.config import DevelopmentConfig,Config
from dash import Dash, html, dcc
# from .dashboard.assets import compile_static_assets
import dash
import dash_bootstrap_components as dbc

from dashboard.header import make_header
external_stylesheets=[dbc.themes.BOOTSTRAP]

import os


def create_app(config_class=Config):
    #import models
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    register_dashapps(app)

    with app.app_context():
        from flask import Blueprint
        dashboard_bp = Blueprint('dashboard_bp', __name__, static_folder="static", static_url_path="/static",
                            template_folder='templates')     
        app.register_blueprint(dashboard_bp)
        
        

    return app


def register_dashapps(app):

    from dashboard.callbacks.callback_handler import register_callbacks as register_callbacks_dashboard
    from dashboard.pages import optimiser  # Import pages
    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    
    dashboard = dash.Dash(__name__,
                        server=app,
                        use_pages=True,
                        url_base_pathname='/',
                        external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.FONT_AWESOME],
                        assets_folder=get_root_path(__name__) + '/assets/',
                        external_scripts = ['https://www.google.com/recaptcha/api.js?render=explicit'],
                        meta_tags=[meta_viewport]
                        )
    # Register pages after app creation
    dash.register_page("optimisation", path="/optimisation", layout=optimiser.layout)

    with app.app_context():
        dashboard.title = 'Zenobe Interview'
        dashboard.layout = html.Div([        
                make_header(),
                dash.page_container
            ])
        register_callbacks_dashboard(dashboard)