from os import path
import re
import pickle
import numpy as np

ALPHABET = ''.join([chr(x) for x in range(ord('а'), ord('я') + 1)]) + 'ё'
SENTENCE_END_CHARS = ".?!:"


def clear_text(text: str, alphabet):
    text = text.lower()
    text = re.sub(f"[^{alphabet}0-9\-\ \.\:\?\!\,]", '', text)

    # I think this can be done with one regex
    for ch in ".!?:":
        text = re.sub(f"\{ch}", f'{ch} ', text)

    text = re.sub("[ ]{2,}", ' ', text)

    text = text.strip()

    return text


class Cum():
    def __init__(self, alphabet=ALPHABET):
        self.alphabet = alphabet
        self.data = dict()
        self.word_start_count = dict()
        self.phrase_end_count = dict()
        self.word_count = dict()

    def fit(self, text):
        text = clear_text(text, self.alphabet)

        def add_one(map, key):
            if key in map:
                map[key] += 1
            else:
                map[key] = 1

        ls = text.split(' ')
        for i in range(len(ls)):

            if i + 1 < len(ls):
                if len(ls[i]) != 0 and ls[i][-1] == ".":
                    add_one(self.word_start_count, ls[i + 1])
            for j in range(1, 3):
                if i + j < len(ls):
                    k = tuple(ls[i:i + j])
                    if not k in self.data:
                        self.data[k] = dict()
                    add_one(self.data[k], ls[i + j])
        for s in ls:
            add_one(self.word_count, s)

    def generate(self, start, length, seed=2086):
        np.random.seed(seed)

        phr = clear_text(start, self.alphabet)
        phr = phr.split(' ')

        def choose_one(map):
            key = list(map)
            val = [map[key[i]] for i in range(len(key))]
            val = np.array(val, dtype="f8")
            val /= np.sum(val)
            return np.random.choice(key, p=val)

        res = " "
        for _ in range(length):
            if len(phr) == 0 or not tuple(phr[-1:]) in self.data:
                if not tuple(phr[-1:]) in self.data:
                    # print("FUCK _1")
                    ...
                word = choose_one(self.word_start_count)
            elif len(phr) == 1 or not tuple(phr[-2:]) in self.data:
                if not tuple(phr[-2:]) in self.data:
                    # print("FUCK _2")
                    ...
                word = choose_one(self.data[tuple(phr[-1:])])
            else:
                word = choose_one(self.data[tuple(phr[-2:])])

            if len(phr) == 0 or len(phr[-1]) == 0 or phr[-1][-1] in SENTENCE_END_CHARS:
                word = word.capitalize()
            res += word + " "

            word = word.lower()
            phr += [word]

        return res


def save_cum(file, cum: Cum):
    with open(file, 'wb') as f:
        pickle.dump(cum, f)


def load_cum(file):
    if path.exists(file):
        with open(file, 'rb') as f:
            res = pickle.load(f)
    else:
        res = Cum()
    return res
