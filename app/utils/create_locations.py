def create_locations(name):
    
    import pickle
        
    with open(name, 'rb') as f:
        locations = pickle.load(f)

    return locations