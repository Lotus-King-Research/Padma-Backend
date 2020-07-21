def view_search_texts(data):

    from flask import render_template

    return render_template('search_texts.html',
                           query=data['query'],
                           title=data['title'],
                           text_title=data['text_title'],
                           text=data['text'],
                           location=data['location'])
