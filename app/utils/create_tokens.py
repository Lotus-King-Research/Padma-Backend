def create_tokens():

    import os
    import pickle
    import sys

    from app import meta

    tokens = {}

    # check if path exist
    if os.path.exists('/tmp/tokens'):
        # handle the case where it's empty
        if len(os.listdir('/tmp/tokens')) == 0:
            _download_tokens()
    # handle the case when the path doesn't exist 
    else:
        _download_tokens()

    # go through the texts
    for filename in meta.keys():

        # get the tokens
        with open('/tmp/tokens/' + filename + '.txt', 'r') as f:
            tokens_temp = f.read()

        # create entry in the tokens dictionary
        tokens[filename] = {'text_title': meta[filename]['title'],
                            'tokens': tokens_temp}

        f.close()

    #print("The size of the dictionary is {} bytes".format(_get_obj_size(tokens)))

    return tokens

def _download_tokens():

    import zipfile
    import wget

    url='https://github.com/Lotus-King-Research/Rinchen-Terdzo-Tokenized/raw/master/tokens/tokens.zip'
    print("Downloading : [Data] Tokens")
    wget.download(url)

    with zipfile.ZipFile('tokens.zip', 'r') as zf:
        zf.extractall('/tmp/tokens/')
