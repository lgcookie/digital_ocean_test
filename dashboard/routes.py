from flask import Blueprint, render_template
from flask import current_app as app

dashboard_bp = Blueprint('dashboard_bp', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/static')

from flask import Blueprint
from .pages import optimiser
from .pages import fleet

def init_routes(app):
    @app.route('/')
    @app.route('/optimisation')
    def optimisation():
        return optimisation(app)

    @app.route('/fleet')
    def fleet():
        return fleet(app)