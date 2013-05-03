__author__ = 'samwing'
from text_statistics import TextStatistics
import re
HAIKU = [5,7,5]
HOKKU = [5,6,4]

def is_haiku(haiku):
    """take a haiku with each line newline delineated and determine whether it is a haiku or not"""
    strings = re.split(r'[\n\r]+', haiku)
    pattern = [TextStatistics(string).count_syllables() for string in strings]
    if pattern == HAIKU:
        return True #japanese haiku
    elif pattern == HOKKU:
        return True #american haiku
    return False

if __name__ == '__main__':
    japanese_haiku = "at the age old pond\na frog leaps into water\na deep resonance"
    assert is_haiku(haiku=japanese_haiku) == True, 'Not a haiku'
