# text_statistics.py
# Sam Wing (2013)
# 1:1 API Fork of TextStatistics.php by Dave Child
# https://github.com/DaveChild/Text-Statistics
import re
def clean_text(text):
    full_stop_tags = ['li', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dd']
    for tag in full_stop_tags:
        text = re.sub(r'</{}>'.format(tag), '.', text)
    replace_with = [('<[^>]+>', ''),    # Strip tags
                    ('[,:;()\-]', ' '), # Replace commans, hyphens etc (count them as spaces)
                    ('[\.!?]', '.'),    # Unify terminators
                    ('^\s+',''),		# Strip leading whitespace
                    ('[\n\r]*', ''),	# Replace new lines with spaces
                    ('[\. ]+','.'),		# Check for duplicated terminators
                    ('\s+', ''),		# Remove multiple spaces
                    ]
    for (regex, replacement) in replace_with:
        text = re.sub(regex, replacement, text)
    return text

if __name__ == '__main__':
    assert clean_text('<h1>Hello!</h1>') == 'Hello.', 'rework the code'