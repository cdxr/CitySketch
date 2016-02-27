# Screen text for sensitive content
import re
from resources.explicit.excluded_words import excluded_words

def sensitive_text(text_input):
    parsed_input = re.split(";|,|\*|\n|#|\\\\|\.|\?|@| ?", text_input)
    # cycle all words and check if sensitive
    for word in parsed_input:
        if sensitive_word(word) == True:
            return True
    return False

def sensitive_word(word):
    if word.lower() in excluded_words:
        return True
    return False

# run just once to populate list of word to be excluded
def populate_bad_words():
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
    populate_bad_words()
