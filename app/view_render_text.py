def view_render_text(data):

    from flask import render_template

    return render_template('render_text.html',
                            text=data['text'],
                            title=data['title'],
                            start=int(data['start']),
                            end=int(data['end']))