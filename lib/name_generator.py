from random import choice, randint
from string import ascii_lowercase
from string import ascii_uppercase


def random_name():
    vowels = 'aeiouy'
    syllables = ''.join(set(ascii_lowercase).difference(vowels))

    name_len = randint(3, 8)
    is_current_vowel = bool(randint(0, 2))

    name = []
    for i in range(name_len):
        if is_current_vowel:
            name.append(choice(vowels))
        else:
            name.append(choice(syllables))

        is_current_vowel = not is_current_vowel

    name[0] = name[0].upper()

    return ''.join(name)
