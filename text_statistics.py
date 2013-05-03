# text_statistics.py
# Sam Wing (2013)
# 1:1 API Fork of TextStatistics.php by Dave Child
# https://github.com/DaveChild/Text-Statistics
from __future__ import division
import re
import sys

from collections import defaultdict

from memoize import memoized

class TextStatistics(object):
    def __init__(self, text):
        self.text = self.clean_text(text=text)

    @staticmethod
    def clean_text(text):
        full_stop_tags = ['li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dd']
        for tag in full_stop_tags:
            text = re.sub(r'</{}>'.format(tag), '.', text)
        replace_with = [('<[^>]+>', ''),    # Strip tags
                        ('[,:;()\-]', ' '), # Replace commans, hyphens etc (count them as spaces)
                        ('[.!?]', '.'),    # Unify terminators
                        ('^\s+',''),		# Strip leading whitespace
                        ('[\n\r]*', ''),	# Replace new lines with spaces
                        ('\.{2,}','.'),		# Check for duplicated terminators
                        ('\s{2,}', ''),		# Remove multiple spaces
                        ]
        for (regex, replacement) in replace_with:
            text = re.sub(regex, replacement, text)
        return text

    def flesch_kincaid_reading_ease(self):
        return round((206.835 - (1.015 * self.average_words_sentence()) - (84.6 * self.average_syllables_word()))*10)/10;

    @memoized
    def average_words_sentence(self):
        return self.word_count() / self.sentence_count()

    @memoized
    def word_count(self):
        return len(self.text.split(' '))

    @memoized
    def sentence_count(self):
        return len(re.findall(r'[.!?]', self.text))


if __name__ == '__main__':
    text_statistics = TextStatistics('<h1>I. Like. Cats.</h1>')
    print text_statistics.average_words_sentence()