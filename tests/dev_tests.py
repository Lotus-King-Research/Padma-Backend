import requests
from time import sleep

end_points = ['http://0.0.0.0:5000/dictionary_lookup?query=པདྨ་འབྱུང་གནས་']

for end_point in end_points:

    r = requests.get(end_point, timeout=30)

    if r.status_code != 200:
        print("FAILED : " + end_point + " failed with status code " + str(r.status_code))
        raise ValueError
    elif r.status_code == 200:
        sleep(3)
        print("PASSED : " + end_point + " with status code 200")