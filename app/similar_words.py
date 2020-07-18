def similar_words(request, dictionary):

    from flask import render_template

    from .pipeline import similar_words

    text = request.args.get('query')
    text = text.replace(' ', '')

    text = similar_words(text, dictionary)

    import pandas as pd

    text = pd.DataFrame(text).reset_index()
    text.columns = ['word', 'similarity']

    return render_template('similar_words.html',
                           text=text.to_html(index=False))