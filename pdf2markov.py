import fitz
import numpy as np

whitelist = set('abcdefghijklmnopqrstuvwxyz ')


# remove everything but lowercase and space
def clean(text):
    return ''.join(filter(whitelist.__contains__, text.lower().replace('\n', ' ').replace(' .', '.')))


# converts lowercase and space to idx
def to_idx(s):
    assert (len(s) == 1)
    if ord(s) >= 97:
        return ord(s) - 97
    else:
        return 26


# creates transition matrix and individual letter probability for digram from text
def to_q(text):
    q = np.zeros((len(whitelist), len(whitelist)))
    p = np.zeros((len(whitelist)))
    p[to_idx(text[0])] += 1
    for i in range(1, len(text)):
        q[to_idx(text[i - 1])][to_idx(text[i])] += 1
        p[to_idx(text[i])] += 1
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = max(q[i][j], 1)  # make sure every point has at least 1 so log doesn't break.
        q[i] = q[i] / sum(q[i])
    return q, p / len(text), text


# loads a file and cleans data
def load_file(filename):
    with fitz.open(filename) as doc:
        data = ""
        for page in doc:
            data += clean(page.get_text())
    return to_q(data)
