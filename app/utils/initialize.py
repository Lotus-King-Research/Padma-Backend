def initialize_dictionary():

    from .create_dictionary import create_dictionary
    dictionary = create_dictionary()
    return dictionary
    

def initialize_vectors():

    from gensim.models import KeyedVectors
    vectors = KeyedVectors.load('app/data/tibetan.vec')
    return vectors