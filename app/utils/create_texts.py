def create_texts():

    '''Creates texts from tokens.'''

    def texts(filename):

        out = {}

        from app import tokens

        tokens_temp = tokens[filename]

        text = ''.join(tokens_temp['tokens'])
        text = text.replace(' ', '')
        
        out = {'text_title': tokens_temp['text_title'],
               'text': text}

        return out

    return texts
