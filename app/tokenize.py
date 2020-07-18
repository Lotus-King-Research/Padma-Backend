def tokenize(request):

    from flask import render_template
    from .pipeline import tokenize

    text = request.args.get('query')

    tokens = tokenize(text)

    return render_template('tokenize.html',
                           tokens=tokens)