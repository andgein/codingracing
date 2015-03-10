__author__ = 'Andrew Gein <andgein@yandex.ru>'

import glob
import random
import string

LANGUAGES = {'csharp': 'C#', 'javascript': 'Javascript'}


def get_code(language):
    assert (language in LANGUAGES.keys())

    pattern = 'codes/%s/*' % language
    files = glob.glob(pattern)
    filename = random.choice(files)

    with open(filename) as f:
        return f.read()


def get_row_and_column(code, position):
    if position is None:
        return {'row': 10000, 'column': 10000}
    row = code[:position].count('\n')
    last_newline = code[:position].rfind('\n')
    column = position - last_newline
    return {'row': row, 'column': column}


def find_diff_position(original_code, code):
    original_idx, idx = 0, 0
    while original_idx < len(original_code) and idx < len(code):
        if original_code[original_idx] in string.whitespace:
            original_idx += 1
        elif code[idx] in string.whitespace:
            idx += 1
        elif original_code[original_idx] == code[idx]:
            original_idx += 1
            idx += 1
        else:
            return idx
    while original_idx < len(original_code) and original_code[original_idx] in string.whitespace:
        original_idx += 1
    while idx < len(code) and code[idx] in string.whitespace:
        idx += 1
    if idx < len(code) or original_idx < len(original_code):
        return idx
    return None