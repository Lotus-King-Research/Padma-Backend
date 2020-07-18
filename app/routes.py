from flask import render_template, request

from app import app

from .pipeline import create_dictionary
from .pipeline import create_texts

dictionary = create_dictionary()
dictionary['source'] = dictionary['source'].str.replace('-', '')
dictionary['source'] = dictionary['source'].str.replace('[', '')
dictionary['source'] = dictionary['source'].str.replace(']', '')

texts = create_texts()

print("SUCCESS: dictionaries built")

@app.after_request
def add_header(r):    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Expires"] = "0"
    r.headers["Pragma"] = "no-cache"

    return r

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dictionary_lookup', methods=['GET','POST'])
def dictionary_lookup():

    from .dictionary_lookup import dictionary_lookup
    return dictionary_lookup(request, dictionary)

@app.route('/search_texts', methods=['GET', 'POST'])
def search_texts():

    from .search_texts import search_texts
    return search_texts(request, texts)

@app.route('/render_text', methods=['GET', 'POST'])
def render_text():

    from .render_text import render_text
    return render_text(request, texts)

@app.route('/render_words', methods=['GET', 'POST'])
def render_words():

    from .render_words import render_words
    return render_words(request, dictionary)

@app.route('/similar_words', methods=['GET', 'POST'])
def similar_words():

    from .similar_words import similar_words
    return similar_words(request, dictionary)

@app.route('/word_statistics', methods=['GET', 'POST'])
def word_statistics():

    from .word_statistics import word_statistics
    return word_statistics(request)

@app.route('/tokenize', methods=['GET', 'POST'])
def tokenize():

    from .tokenize import tokenize
    return tokenize(request)


