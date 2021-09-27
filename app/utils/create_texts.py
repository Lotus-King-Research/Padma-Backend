def create_texts():

    '''Creates texts from tokens.'''

    def texts(filename):

        out = {}

        from app import tokens

        text = ''.join(tokens[filename]['tokens'])
        text = text.replace(' ', '')
        
        out = {'text_title': tokens[filename]['text_title'],
               'text': text}

        return out

    return texts
