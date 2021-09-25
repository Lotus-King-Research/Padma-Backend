def create_texts():

    import os
    import pickle

    texts = {}

    with open('app/data/title_info.pkl', 'rb') as f:
        meta = pickle.load(f)

    for key in meta.keys():
    
        with open('/tmp/docs/' + key + '.txt', 'r') as f:
            text = f.readlines()

        texts[key] = {'text_title': meta[key]['title'],
                      'text': text}

        f.close()

    return texts