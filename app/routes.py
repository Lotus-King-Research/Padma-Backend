from flask import render_template, request

from app import app

from .utils.initialize import initialize

dictionary, texts = initialize()

print("SUCCESS: assets built")

@app.after_request
def add_header(r):    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Expires"] = "0"
    r.headers["Pragma"] = "no-cache"

    return r

@app.route('/dictionary_lookup', methods=['GET','POST'])
def dictionary_lookup():

    from .models.dictionary_lookup import dictionary_lookup

    return dictionary_lookup(request, dictionary)

@app.route('/search_texts', methods=['GET', 'POST'])
def search_texts():

    from .models.search_texts import search_texts

    return search_texts(request, texts)

@app.route('/find_similar', methods=['GET', 'POST'])
def find_similar():

    from .models.find_similar import find_similar

    return find_similar(request, dictionary)

@app.route('/word_statistics', methods=['GET', 'POST'])
def word_statistics():

    from .models.word_statistics import word_statistics
    
    return word_statistics(request, texts)

@app.route('/tokenize', methods=['GET', 'POST'])
def tokenize():

    from .models.tokenize import tokenize

    return tokenize(request)

@app.route('/render_text', methods=['GET', 'POST'])
def render_text():

    from .models.render_text import render_text

    return render_text(request, texts)

@app.route('/frequent_words', methods=['GET', 'POST'])
def frequent_words():

    from .models.frequent_words import frequent_words

    return frequent_words(request, texts)
