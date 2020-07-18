def render_words(request, dictionary):

    from flask import render_template

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