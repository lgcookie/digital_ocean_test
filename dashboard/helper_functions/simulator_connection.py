# echo-client.py
import requests
import json 
def simulator_connection(user_params):
    try:
        public= f'http://167.172.181.221:8000/simulation_{user_params["simulation_type"]}'
        private = f'http://0.0.0.0:8000/simulation_{user_params["simulation_type"]}'
        response = requests.post(public,json=user_params,timeout=20)
        resp=response.json()
        resp_message = json.loads(resp)["response_message"]

    except requests.exceptions.ReadTimeout: 
        resp_message = f'Our simulator is working on it, please give it a few minutes, refresh the page, and your {user_params["simulation_type"]} simulation: {user_params["simulation_name"]}, will be automatically uploaded.'
    except Exception as e:
        resp_message = "Our simulator server has malfunctioned, sorry about this."
    finally:
        return resp_message