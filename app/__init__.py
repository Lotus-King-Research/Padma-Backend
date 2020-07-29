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

import enchant
import en_core_web_sm

nlp = en_core_web_sm.load()

enchant_word_check = enchant.Dict("en")

from botok import Text

from app import routes

# ༈ བློ་ཆོས་སུ་འགྲོ་བར་བྱིན་གྱིས་རློབས། །ཆོས་ལམ་དུ་འགྲོ་བར་བྱིན་གྱིས་རློབས། །ལམ་འཁྲུལ་བ་ཞིག་པར་བྱིན་གྱིས་རློབས། །འཁྲུལ་པ་ཡེ་ཤེས་སུ་འཆར་བར་བྱིན་གྱིས་རློབས། །

# below is for debugging only

#app.jinja_env.auto_reload = True
#app.config['TEMPLATES_AUTO_RELOAD'] = True

# try first docker, then gunicorn, and
# then flask if all else fails. Handle 
# tricky debugs at flask level to 
# minimize complexity.

#FLASK_APP=app.py FLASK_ENV=development flask run
#gunicorn server:app --access-logfile /tmp/gunicorn-access.log --error-logfile /tmp/gunicorn-error.log --worker-tmp-dir /dev/shm --worker-class gevent --timeout 120 -b 0.0.0.0:5000 -w 2 --preload