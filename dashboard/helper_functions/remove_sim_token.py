from flaskproperty import db
from flask_login import current_user

def remove_sim_token():
    current_user.num_simulations_left = current_user.num_simulations_left-1
    db.session.commit()
    return "removed a simulation token from the user" 