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

    from .pipeline import definition_lookup
    from .pipeline import tokenize

    search_query = request.args.get('query')
    no_of_result = request.args.get('no_of_result')

    if search_query is None:
        search_query = request.form['query']

    search_query = search_query.replace(' ', '')

    tokens = tokenize(search_query)

    print(tokens)
    print(type(no_of_result))

    results = []

    for token in tokens:
        result = definition_lookup(token, dictionary)
        result.columns = [token, 'source']

        if isinstance(no_of_result, str):
            result = result.iloc[:int(no_of_result)]
            
        
        results.append(result.to_html(index=False))

    return render_template('dictionary_lookup.html',
                            search_query=search_query,
                            results=results,
                            tokens=tokens,
                            results_len=list(range(len(results))))

@app.route('/search_texts', methods=['GET', 'POST'])
def search_texts():

    from .pipeline import search_texts
    from .pipeline import tokenize

    search_query = request.args.get('query')
    #no_of_result = request.args.get('no_of_result')

    if search_query is None:
        search_query = request.form['query']

    #tokens = tokenize(search_query)

    results = search_texts(search_query, texts)

    return render_template('search_texts.html',
                            search_query=search_query,
                            titles=list(texts.keys()),
                            results=results,
                            results_len=list(range(len(results))))

@app.route('/render_text', methods=['GET', 'POST'])
def render_text():

    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')

    text = ''.join(texts[title]).split()
    text = ''.join(text[int(start):int(end)])

    return render_template('render_text.html',
                            title=title,
                            text=text,
                            start=int(start),
                            end=int(end))
