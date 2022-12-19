from flask import Flask
from controller import nsolar_controller

APP = Flask(__name__)

APP.register_blueprint(nsolar_controller.get_blueprint(), url_prefix='/nsolar')

if __name__ == "__main__":
    APP.run(debug=True, port=4000)
