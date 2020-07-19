def view_render_words(data):

    from flask import render_template

    return render_template('render_words.html', data=data)