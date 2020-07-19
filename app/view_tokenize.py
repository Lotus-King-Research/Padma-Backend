def view_tokenize(data):

    from flask import render_template

    return render_template('tokenize.html',
                           tokens=data['tokens'])