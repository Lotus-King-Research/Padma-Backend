import pandas as pd
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['https://staging.padma.io',
           'http://staging.padma.io',
           'https://padma.io',
           'http://padma.io',
           'https://test.padma.io',
           'http://test.padma.io',
           'https://staging.padma.io:8080',
           'http://staging.padma.io:8080',
           'https://padma.io:8080',
           'http://padma.io:8080',
           'https://test.padma.io:8080',
           'http://test.padma.io:8080',
           'https://localhost:8080',
           'http://localhost:8080',
           'chrome-extension://ckndbdjoogkmkledkdfclanamfodcbpe',
           'chrome-extension://hmjfaebolfifcpopioomhbpnpjgdcelb']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.utils.initialize import initialize_dictionary
from app.utils.initialize import initialize_vectors
from app.utils.tokenization import init_tokenizer

dictionary = initialize_dictionary()
vectors = initialize_vectors()
tokenizer = init_tokenizer()

_base_url = 'https://raw.githubusercontent.com/Lotus-King-Research/Padma-Dictionary-Data/main/data/'
available_dictionaries = pd.read_csv(_base_url + 'dictionaries.csv')['Label'].tolist()

from botok import Text

from app import routes
