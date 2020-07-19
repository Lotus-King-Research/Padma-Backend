from flask import render_template, request

from app import app

from .initialize import initialize
from .pipeline import create_dictionary
from .pipeline import create_texts

initialize()
dictionary = create_dictionary()
texts = create_texts()

print("SUCCESS: assets built")

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
    from .view_dictionary_lookup import view_dictionary_lookup

    # produce the data
    data = dictionary_lookup(request, dictionary)
    
    if request.args.get('mode') == 'api':
        return data
    else:
        # render view
        return view_dictionary_lookup(data)

@app.route('/search_texts', methods=['GET', 'POST'])
def search_texts():

    from .search_texts import search_texts
    from .view_search_texts import view_search_texts

    data = search_texts(request, texts)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_search_texts(data)

@app.route('/find_similar', methods=['GET', 'POST'])
def render_text():

    from .find_similar import find_similar
    from .view_find_similar import view_find_similar

    data = find_similar(request, texts)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_find_similar(data)

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


