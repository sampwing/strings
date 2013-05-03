__author__ = 'samwing'
from text_statistics import TextStatistics
import re
HAIKU = [5,7,5]

def is_haiku(haiku):
    strings = re.split(r'[\n\r]+', haiku)
    return [TextStatistics(string).count_syllables() for string in strings] == HAIKU

if __name__ == '__main__':
    haiku = "at the age old pond\na frog leaps into water\na deep resonance"
    assert is_haiku(haiku=haiku) == True, 'Not a haiku'
