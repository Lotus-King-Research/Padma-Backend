# coding=utf-8

# TEST THE API ENDPOINTS

import requests

end_points = ['http://padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://padma.io/search_texts?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://padma.io/find_similar?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://padma.io/word_statistics?query=པདྨ་&mode=api',
              'http://padma.io/tokenize?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://padma.io/render_text?title=Terdzo-ZI-052&start=2&end=4&mode=api']

for end_point in end_points:

    r = requests.post(end_point, timeout=15)

    if r.status_code != 200:
        print("ERROR: the request " + end_point + " failed with status code" + str(r.status_code))
        raise ValueError
