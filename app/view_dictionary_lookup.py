def view_dictionary_lookup(data):

    from flask import render_template

    return render_template('dictionary_lookup.html',
                           query=data['search_query'],
                           text=data['text'],
                           source=data['source'],
                           tokens=data['tokens'])
