from itertools import chain
import json
import re


class Word:
    """container for word-based methods"""

    __slots__ = ["slices", "word", "alphabet", "only_replacements"]  # optimization

    def __init__(self, word, only_replacements=False):
        """
        Generate slices to assist with typo
        definitions.

        'the' => (('', 'the'), ('t', 'he'),
                  ('th', 'e'), ('the', ''))

        """
        slice_range = range(len(word) + 1)
        self.slices = tuple((word[:i], word[i:]) for i in slice_range)
        self.word = word
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.only_replacements = only_replacements

    def _deletes(self):
        """th"""
        for a, b in self.slices[:-1]:
            yield "".join((a, b[1:]))

    def _transposes(self):
        """teh"""
        for a, b in self.slices[:-2]:
            yield "".join((a, b[1], b[0], b[2:]))

    def _replaces(self):
        """tge"""
        for a, b in self.slices[:-1]:
            for c in self.alphabet:
                yield "".join((a, c, b[1:]))

    def _inserts(self):
        """thwe"""
        for a, b in self.slices:
            for c in self.alphabet:
                yield "".join((a, c, b))

    def typos(self):
        """letter combinations one typo away from word"""
        if self.only_replacements:
            return chain(self._replaces())
        else:
            return chain(
                self._deletes(), self._transposes(), self._replaces(), self._inserts()
            )

    def double_typos(self):
        """letter combinations two typos away from word"""
        return chain.from_iterable(
            Word(e1, only_replacements=self.only_replacements).typos()
            for e1 in self.typos()
        )

class Speller:
    def __init__(
        self, lang="en", threshold=0, nlp_data=None, fast=False, only_replacements=False
    ):
        self.lang = lang
        self.threshold = threshold
        with open("word_count.json", "r") as f:
            self.nlp_data = json.load(f)
        self.fast = fast
        self.only_replacements = only_replacements

        if threshold > 0:
            # print(f'Original number of words: {len(self.nlp_data)}')
            self.nlp_data = {k: v for k, v in self.nlp_data.items() if v >= threshold}
            # print(f'After applying threshold: {len(self.nlp_data)}')

    def existing(self, words):
        """{'the', 'teh'} => {'the'}"""
        return {word for word in words if word in self.nlp_data}

    def get_candidates(self, word):
        w = Word(word, self.only_replacements)
        if self.fast:
            candidates = self.existing([word]) or self.existing(w.typos()) or [word]
        else:
            candidates = (
                self.existing([word])
                or self.existing(w.typos())
                or self.existing(w.double_typos())
                or [word]
            )
        return [(self.nlp_data.get(c, 0), c) for c in candidates]

    def autocorrect_word(self, word):
        """most likely correction for everything up to a double typo"""
        if word == "":
            return ""

        candidates = self.get_candidates(word)

        # in case the word is capitalized
        if word[0].isupper():
            decapitalized = word[0].lower() + word[1:]
            candidates += self.get_candidates(decapitalized)

        best_word = max(candidates)[1]

        if word[0].isupper():
            best_word = best_word[0].upper() + best_word[1:]
        return best_word

    def autocorrect_sentence(self, sentence):
        return re.sub(
            r"[A-Za-z]+",
            lambda match: self.autocorrect_word(match.group(0)),
            sentence,
        )

    __call__ = autocorrect_sentence
    
    
