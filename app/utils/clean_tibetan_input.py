def clean_tibetan_input(s):

    s = s.replace(' ', '')
    s = s.replace(' ', '')
    s = s.rstrip()
    s = s.lstrip()

    if s.endswith('།'):
        s = s.replace('།', '་')
    
    elif s.endswith('༔'):
        s = s.replace('༔', '་')
        
    elif s.endswith('་'):
        pass
    
    else:
        s += '་'
        
    s = s.replace('་་', '་')

    return s