import requests
from time import sleep

end_points = ['http://api.padma.io/dictionary_lookup?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://api.padma.io/search_texts?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://api.padma.io/find_similar?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://api.padma.io/word_statistics?query=པདྨ་&mode=api',
              'http://api.padma.io/tokenize?query=པདྨ་འབྱུང་གནས་&mode=api',
              'http://api.padma.io/render_text?title=Terdzo-ZI-052&start=2&end=4&mode=api']

for end_point in end_points:

    r = requests.post(end_point, timeout=15)

    if r.status_code != 200:
        print("ERROR: the request " + end_point + " failed with status code" + str(r.status_code))
        raise ValueError

    sleep(2)
