import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)

from app.utils.initialize import initialize_meta
from app.utils.initialize import initialize_dictionary
from app.utils.initialize import initialize_tokens
from app.utils.initialize import initialize_texts
from app.utils.initialize import initialize_index
from app.utils.initialize import initialize_locations

from app.utils.text_search import text_search
from app.utils.tokenization import init_tokenizer

meta = initialize_meta()
dictionary = initialize_dictionary()
tokens = initialize_tokens()
texts = initialize_texts()
index = initialize_index()
locations = initialize_locations()

tokenizer = init_tokenizer()

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


