from flask import Flask
from controller import nsolar_controller
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

#settings 
APP.secret_key = 'mysecretkey'

APP.register_blueprint(nsolar_controller.get_blueprint(), url_prefix='/nsolar')

if __name__ == "__main__":
    APP.run(debug=True, port=4000)
