import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.utils.initialize import initialize_dictionary
from app.utils.tokenization import init_tokenizer

dictionary = initialize_dictionary()
tokenizer = init_tokenizer()

# Default source list (order = dictionaries.csv order, preserved at build time),
# so `dictionaries[0]` defaults match the previous pandas implementation.
available_dictionaries = list(dictionary.dictionaries.keys())

from app import routes

# Co-host the built frontend SPA as static files on the same origin, so the
# whole app is one service. Disabled if the directory is absent (API-only).
_FRONTEND_DIR = os.environ.get("PADMA_FRONTEND", "frontend")
if os.path.isdir(_FRONTEND_DIR):
    from fastapi.staticfiles import StaticFiles
    app.mount("/", StaticFiles(directory=_FRONTEND_DIR, html=True), name="frontend")
