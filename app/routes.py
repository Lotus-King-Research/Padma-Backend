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

    if len(search_query) == 0:
        search_query = dictionary['word'].sample(1).values[0]
        print(len(search_query))

    search_query = search_query.replace(' ', '')

    tokens = tokenize(search_query)

    results = []

    for token in tokens:
        try:
            result = definition_lookup(token, dictionary)
        except ValueError:
            return render_template('oops.html')
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


@app.route('/render_words', methods=['GET', 'POST'])
def render_words():

    from .pipeline import dict_for_render_words
    from .pipeline import similar_words

    word = request.args.get('query')
    word = word.replace(' ', '')

    text = similar_words(word, dictionary)
    text = text.reset_index()

    data = {}

    for i, key in enumerate(text[text.columns[0]].values):
        data[key.text] = text[text.columns[1]].values[i]
        
    data = dict_for_render_words(data, word)
    
    return render_template('render_words.html', data=data)


@app.route('/similar_words', methods=['GET', 'POST'])
def similar_words():

    from .pipeline import similar_words

    text = request.args.get('query')
    text = text.replace(' ', '')

    text = similar_words(text, dictionary)

    import pandas as pd

    text = pd.DataFrame(text).reset_index()
    text.columns = ['word', 'similarity']

    return render_template('similar_words.html',
                           text=text.to_html(index=False))


@app.route('/word_statistics', methods=['GET', 'POST'])
def word_statistics():

    from .word_statistics import word_statistics
    import os
    import pandas as pd

    query = request.args.get('query')

    prominence = word_statistics(query, os.listdir('/tmp/tokens'), 'prominence')
    co_occurance = word_statistics(query, os.listdir('/tmp/tokens'), 'co_occurance')
    most_common = word_statistics(query, os.listdir('/tmp/tokens'), 'most_common')

    prominence = pd.DataFrame(pd.Series(prominence)).head(30).reset_index()
    co_occurance = pd.DataFrame(pd.Series(co_occurance)).head(30).reset_index()
    most_common = pd.DataFrame(pd.Series(most_common)).head(30).reset_index()

    prominence.columns = ['title', 'prominence']
    co_occurance.columns = ['word', 'co_occurancies']
    most_common.columns = ['word', 'occurancies']

    prominence['title'] = [i[0] for i in prominence['prominence']]
    prominence['prominence'] = [i[1] for i in prominence['prominence']]

    prominence = prominence.sort_values('prominence', ascending=False)

    prominence = prominence.to_html(index=False)
    co_occurance = co_occurance.to_html(index=False)
    most_common = most_common.to_html(index=False)

    return render_template('word_statistics.html',
                           prominence=prominence,
                           co_occurance=co_occurance,
                           most_common=most_common)

@app.route('/tokenize', methods=['GET', 'POST'])
def tokenize():

    from .pipeline import tokenize

    text = request.args.get('query')

    tokens = tokenize(text)

    return render_template('tokenize.html',
                           tokens=tokens)
