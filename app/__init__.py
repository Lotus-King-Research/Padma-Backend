from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app.utils.initialize import initialize_dictionary
from app.utils.initialize import initialize_texts
from app.utils.initialize import initialize_tokens

dictionary = initialize_dictionary()
texts = initialize_texts()
tokens = initialize_tokens()

from botok import Text

from app import routes

#app.jinja_env.auto_reload = True
#app.config['TEMPLATES_AUTO_RELOAD'] = True

# ༈ བློ་ཆོས་སུ་འགྲོ་བར་བྱིན་གྱིས་རློབས། །ཆོས་ལམ་དུ་འགྲོ་བར་བྱིན་གྱིས་རློབས། །ལམ་འཁྲུལ་བ་ཞིག་པར་བྱིན་གྱིས་རློབས། །འཁྲུལ་པ་ཡེ་ཤེས་སུ་འཆར་བར་བྱིན་གྱིས་རློབས། །