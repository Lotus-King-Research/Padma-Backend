# coding=utf-8

# TEST THE API ENDPOINTS

import requests

end_points = ['http://0.0.0.0:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://0.0.0.0:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://0.0.0.0:5000/search_texts?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://0.0.0.0:5000/find_similar?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://0.0.0.0:5000/word_statistics?query=པདྨ་&mode=api',
              'http://0.0.0.0:5000/tokenize?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://0.0.0.0:5000/render_text?title=Terdzo-ZI-052&start=2&end=4&mode=api']

for end_point in end_points:

    r = requests.get(end_point, timeout=5)

    if r.status_code != 200:
        print("ERROR: the request " + end_point + " failed with status code" + str(r.status_code))
        raise ValueError

