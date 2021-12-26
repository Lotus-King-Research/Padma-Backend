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

# search_texts

@app.get('/search_texts')
def search_texts(request: Request):

    from .models.search_texts import search_texts

    return search_texts(request)

@app.post('/search_texts')
def search_texts(request: Request):

    from .models.search_texts import search_texts

    return search_texts(request)

# render_text

@app.get('/render_text')
def render_text(request: Request):

    from .models.render_text import render_text

    return render_text(request)

@app.post('/render_text')
def render_text(request: Request):

    from .models.render_text import render_text

    return render_text(request)

# word_statistics

@app.get('/word_statistics')
def word_statistics(request: Request):

    from .models.word_statistics import word_statistics
    
    return word_statistics(request)

@app.post('/word_statistics')
def word_statistics(request: Request):

    from .models.word_statistics import word_statistics
    
    return word_statistics(request)

# tokenize

@app.get('/tokenize')
def tokenize(request: Request):

    from .models.tokenize import tokenize

    return tokenize(request)

@app.post('/tokenize')
def tokenize(request: Request):

    from .models.tokenize import tokenize

    return tokenize(request)