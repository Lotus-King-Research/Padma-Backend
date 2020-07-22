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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/dictionary_lookup', methods=['GET','POST'])
def dictionary_lookup():

    from .pipelines.dictionary_lookup import dictionary_lookup
    from .views.view_dictionary_lookup import view_dictionary_lookup

    # produce the data
    data = dictionary_lookup(request, dictionary)
    
    if request.args.get('mode') == 'api':
        return data
    else:
        # render view
        return view_dictionary_lookup(data)

@app.route('/search_texts', methods=['GET', 'POST'])
def search_texts():

    from .pipelines.search_texts import search_texts
    from .views.view_search_texts import view_search_texts

    data = search_texts(request, texts)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_search_texts(data)

@app.route('/find_similar', methods=['GET', 'POST'])
def find_similar():

    from .pipelines.find_similar import find_similar
    from .views.view_find_similar import view_find_similar

    data = find_similar(request, dictionary)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_find_similar(data)

@app.route('/word_statistics', methods=['GET', 'POST'])
def word_statistics():

    from .pipelines.word_statistics import word_statistics
    from .views.view_word_statistics import view_word_statistics
    
    data = word_statistics(request, texts)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_word_statistics(data)

@app.route('/tokenize', methods=['GET', 'POST'])
def tokenize():

    from .pipelines.tokenize import tokenize
    from .views.view_tokenize import view_tokenize

    data = tokenize(request)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_tokenize(data)

@app.route('/render_text', methods=['GET', 'POST'])
def render_text():

    from .pipelines.render_text import render_text
    from .views.view_render_text import view_render_text

    data = render_text(request, texts)

    if request.args.get('mode') == 'api':
        return data
    else:
        return view_render_text(data)