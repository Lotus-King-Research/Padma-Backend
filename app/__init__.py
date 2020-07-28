from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from app.utils.initialize import initialize

dictionary, texts = initialize()

from app import routes

#app.jinja_env.auto_reload = True
#app.config['TEMPLATES_AUTO_RELOAD'] = True

