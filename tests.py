# coding=utf-8

# TEST THE API ENDPOINTS

import requests

end_points = ['http://127.0.0.1:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://127.0.0.1:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://127.0.0.1:5000/search_texts?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://127.0.0.1:5000/find_similar?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://127.0.0.1:5000/word_statistics?query=པདྨ་&mode=api',
              'http://127.0.0.1:5000/tokenize?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://127.0.0.1:5000/render_text?title=Terdzo-ZI-052&start=2&end=4&mode=api']

for end_point in end_points:

    r = requests.get(end_point)

    if r.status_code != 200:
        print("ERROR: the request " + end_point + " failed with status code" + r.status_code)
        raise ValueError

