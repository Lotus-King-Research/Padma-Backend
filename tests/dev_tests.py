import requests
from time import sleep

end_points = ['http://0.0.0.0:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་',
              'http://0.0.0.0:5000/search_texts?query=པདྨ་འབྱུང་གནས་',
              'http://0.0.0.0:5000/find_similar?query=པདྨ་འབྱུང་གནས་',
              'http://0.0.0.0:5000/word_statistics?query=པདྨ་',
              'http://0.0.0.0:5000/tokenize?query=པདྨ་འབྱུང་གནས་',
              'http://0.0.0.0:5000/render_text?title=Terdzo-ZI-052&start=2&end=4']

for end_point in end_points:

    r = requests.get(end_point, timeout=30)

    if r.status_code != 200:
        print("FAILED : " + end_point + " failed with status code " + str(r.status_code))
        raise ValueError
    elif r.status_code == 200:
        sleep(3)
        print("PASSED : " + end_point + " with status code 200")