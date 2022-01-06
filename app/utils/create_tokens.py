def create_tokens():

    import os
    import pickle
    import sys

    from app import meta

    tokens = {}

    if os.path.exists('/tmp/tokens') is False:
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
    print("Downloading tokens:")
    wget.download(url)

    with zipfile.ZipFile('tokens.zip', 'r') as zf:
        zf.extractall('/tmp/tokens/')
