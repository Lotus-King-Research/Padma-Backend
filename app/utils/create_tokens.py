def create_tokens():

    import os
    #from .stopword import stopword_tibetan

    tokens = {}

    for filename in os.listdir('/tmp/tokens'):

        f = open('/tmp/tokens/' + filename, 'r')
        tokens_temp = f.read()
        tokens_temp = tokens_temp.split()
        #tokens_temp = stopword_tibetan(tokens_temp)
        tokens[filename] = tokens_temp
        
        f.close()

    return tokens