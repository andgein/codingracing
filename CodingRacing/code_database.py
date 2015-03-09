__author__ = 'Andrew Gein <andgein@yandex.ru>'

import glob
import random

LANGUAGES = {'csharp': 'C#', 'javascript': 'Javascript'}


def get_code(language):
    assert (language in LANGUAGES.keys())

    pattern = 'codes/%s/*' % language
    files = glob.glob(pattern)
    filename = random.choice(files)

    with open(filename) as f:
        return f.read()
