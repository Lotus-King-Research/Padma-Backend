from fastapi import Request

from app import app

# dictionary_lookup

@app.get('/dictionary_lookup')
def dictionary_lookup(request: Request):

    from .models.dictionary_lookup import dictionary_lookup

    return dictionary_lookup(request)

@app.post('/dictionary_lookup')
def dictionary_lookup(request: Request):

    from .models.dictionary_lookup import dictionary_lookup

    return dictionary_lookup(request)
