# text_statistics.py
# Sam Wing (2013)
# 1:1 API Fork of TextStatistics.php by Dave Child
# https://github.com/DaveChild/Text-Statistics
from __future__ import division
import re

from memoize import memoized

class TextStatistics(object):
    def __init__(self, text):
        self.text = self.clean_text(text=text)

    @staticmethod
    def clean_text(text):
        full_stop_tags = ['li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dd']
        for tag in full_stop_tags:
            text = re.sub(r'</{}>'.format(tag), '. ', text)
        replace_with = [('<[^>]+>', ''),    # Strip tags
                        ('[,:;()\-]', ' '), # Replace commans, hyphens etc (count them as spaces)
                        ('[.!?]', '.'),    # Unify terminators
                        ('^\s+',''),		# Strip leading whitespace
                        ('[\n\r]+', ''),	# Replace new lines with spaces
                        ('\.{2,}','.'),		# Check for duplicated terminators
                        ('\s{2,}', ' '),		# Remove multiple spaces
                        ]
        for (regex, replacement) in replace_with:
            text = re.sub(regex, replacement, text)
        return text

    def flesch_kincaid_reading_ease(self):
        return round((206.835 - (1.015 * self.average_words_sentence())
                      - (84.6 * self.average_syllables_word())) * 10) / 10

    def flesch_kincaid_grade_level(self):
        return round(((0.39 * self.average_words_sentence())
                      + (11.8 * self.average_syllables_word()) - 15.59) * 10) / 10

    def gunning_fog_score(self):
        return round(((self.average_words_sentence() + self.percentage_words_three_syllables()) * 0.4) * 10) / 10

    def coleman_liau_index(self):
        return round(((5.89 * self.letter_count() / (self.word_count() + 1))
                      - (0.3 * self.sentence_count() / (self.word_count() or 1)) - 15.8 ) *10) / 10

    def smog_index(self):
        return round(1.043 * ((self.words_three_syllables() * (30 / (self.sentence_count() or 1)))
                              + 3.1291)**.5 * 10) / 10

    def automated_readability_index(self):
        return round(((4.71 * (self.letter_count() / self.word_count()))
                      + (0.5 * (self.word_count() / (self.sentence_count() + 1))) - 21.43) * 10) / 10

    @memoized
    def letter_count(self):
        return len(re.sub(r'[^a-zA-Z]+', '', self.text))

    @memoized
    def percentage_words_three_syllables(self, count_proper_nouns=False):
        return self.words_three_syllables() / (self.word_count() or 1) * 100

    @memoized
    def words_three_syllables(self, count_proper_nouns=False):
        words_with_three_syllables = 0
        for word in re.split(r'\s+', self.text):
            if re.match(r'^[A-Z]', word) or count_proper_nouns == True:
                if self.syllable_count(word=word) > 2:
                    words_with_three_syllables += 1
        return words_with_three_syllables

    @memoized
    def average_words_sentence(self):
        return self.word_count() / (self.sentence_count() or 1)

    @memoized
    def word_count(self):
        return len(self.text.split(' '))

    @memoized
    def sentence_count(self):
        return len(re.findall(r'[.!?]', self.text))

    @memoized
    def average_syllables_word(self):
        syllable_count = 0
        word_count = self.word_count()
        for word in re.split(r'\s+', self.text):
            syllable_count += self.syllable_count(word=word)
        return (syllable_count or 1) / (word_count or 1)

    def count_syllables(self):
        syllables = 0
        for word in re.split(r'\s+', self.text):
            syllables += self.syllable_count(word=word)
        return syllables

    @staticmethod
    def syllable_count(word):
        problem_words = {'simile': 3,
                         'forever': 3,
                         'shoreline': 2
                        }
        word = re.sub(r'[^a-z]', '', word.lower())
        if word in problem_words:
            return problem_words[word]
        sub_syllables = ['cial',
                         'tia',
                         'cius',
                         'cious',
                         'giu',
                         'ion',
                         'iou',
                         'sia$',
                         '[^aeiouyt]{2,}ed$',
                         '.ely$',
                         '[cg]h?e[rsd]?$',
                         'rved?$',
                         '[aeiouy][ds]es?$',
                         '[aeiouy][^aeiouydt]e[rsd]?$',
                         '^[dr]e[aeiou][^aeiou]+$',
                         '[aeiouy]rse$',
                         ]
        add_syllables = [
            'ia',
            'riet',
            'dien',
            'iu',
            'io',
            'ii',
            '[aeiouym]bl$',
            '[aeiou]{3}',
            '^mc',
            'ism$',
            '([^aeiouy])\1l$',
            '[^l]lien',
            '^coa[dglx].',
            '[^gq]ua[^auieo]',
            'dnt$',
            'uity$',
            'ie(r|st)$'
        ]
        prefix_suffix = [
            '^un',
            '^fore',
            'ly$',
            'less$',
            'ful$',
            'ers?$',
            'ings?$',
        ]
        prefix_suffix_count = 0
        for regex in prefix_suffix:
            if re.search(regex, word):
                word = re.sub(regex, '', word)
                prefix_suffix_count += 1
        word_part_count = len(filter(None, re.split(r'[^aeiouy]+', word)))
        syllable_count = word_part_count + prefix_suffix_count
        for syllable in sub_syllables:
            if re.search(syllable, word):
                syllable_count -= 1
        for syllable in add_syllables:
            if re.search(syllable, word):
                syllable_count += 1
        return syllable_count or 1


if __name__ == '__main__':
    text_statistics = TextStatistics('The Australian platypus is seemingly a hybrid of a mammal and reptilian creature.')
    print text_statistics.average_words_sentence()
    print text_statistics.flesch_kincaid_reading_ease()
    print text_statistics.flesch_kincaid_grade_level()
    print text_statistics.gunning_fog_score()
    print text_statistics.coleman_liau_index()
    print text_statistics.smog_index()
    print text_statistics.automated_readability_index()