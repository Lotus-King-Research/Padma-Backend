def render_text(request, texts):

    from flask import render_template

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