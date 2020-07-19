def view_word_statistics(data):

    from flask import render_template

    return render_template('word_statistics.html',
                           prominence_key=data['prominence_key'],
                           prominence_value=data['prominence_value'],
                           co_occurance_key=data['co_occurance_key'],
                           co_occurance_value=data['co_occurance_value'],
                           most_common_key=data['most_common_key'],
                           most_common_value=data['most_common_value'])