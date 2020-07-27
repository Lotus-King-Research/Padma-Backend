def initialize():

    import os

    from .create_dictionary import create_dictionary
    from .create_texts import create_texts

    dictionary = create_dictionary()
    texts = create_texts()

    return dictionary, texts