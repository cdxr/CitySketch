# Screen text for sensitive content
import re
from resources.explicit.excluded_words import excluded_words



"""
Determine if the given string contains any sensitive words.
"""
def sensitive_text(text_input):
    parsed_input = re.split(";|,|\*|\n|#|\\\\|\.|\?|@| ?", text_input)

    # cycle all words and check if sensitive
    return any(sensitive_word(word) for word in parsed_input)


"""
Determine if the given string is found in the set of sensitive words.

"""
def sensitive_word(word):
    return word.lower() in _sensitive_word_set




# The immutable set of words that should be considered sensitive.

# A frozenset is used instead of a list because inclusion in a frozenset can
# be tested in constant time.
_sensitive_word_set = frozenset(excluded_words)


# Create a python module that provides a list of sensitive words.
# The module is written to "resources/explicit/excluded_words.py".
#
# Run just once to populate the list.
#
def _populate_bad_words():
    excluded_words = []
    # list 1
    excluded_words += bad_list
    # list 2
    with open('resources/explicit/shutterstock-github/en') as f:
        bad_list2 = f.read().splitlines()
    excluded_words += bad_list2
    excluded_words.sort()
    # output to file
    file = open('resources/explicit/excluded_words.py', 'w')
    file.write('excluded_words = [')
    for word in excluded_words:
        file.write("\'" + word + "\',")
    file.write(']')
    file.close()

if __name__ == '__main__':
    _populate_bad_words()
