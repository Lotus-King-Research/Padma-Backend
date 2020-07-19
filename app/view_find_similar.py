def view_find_similar(data):

    from flask import render_template

    return render_template('find_similar.html', data=data)