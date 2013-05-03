def my_hash(string):
    return sum([(0b1 << index) * ord(character) for (index, character) in enumerate(string)])

def search_and_match(string_to_match, text_to_search):
    """return a list of indices found within text_to_search that match string_to_match"""
    original_hashed_value = my_hash(string=string_to_match)
    match_length = len(string_to_match)
    hashed_value = my_hash(string=text_to_search[:match_length])
    matches = list()
    if hashed_value == original_hashed_value:
        matches.append(0)
    for index in xrange(1, len(text_to_search) - match_length + 1):
        hashed_value -= 2**0 * ord(text_to_search[index - 1])
        hashed_value /= 2
        hashed_value += 2**(match_length -1) * ord(text_to_search[index + match_length - 1])
        if hashed_value == original_hashed_value:
            matches.append(index)
    return matches

def test():
    import re
    string = 'string'
    text = 'string string'
    known_locations = [match.start() for match in re.finditer(string, text)]
    result = search_and_match(string_to_match=string, text_to_search=text) 
    assert result == known_locations, 'error in code logic'

if __name__ == '__main__':
    test()
    
