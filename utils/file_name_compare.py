import re
import numpy as np


def extract_letters(filename):
    letters = re.findall('([a-zA-Z]+)', filename)
    return ''.join(letters)


def compare_filenames(filename1, filename2):
    letters1 = extract_letters(filename1)
    letters2 = extract_letters(filename2)
    if letters1 in letters2:
        return True

    else:
        return False
