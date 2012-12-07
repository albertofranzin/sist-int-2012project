#!/usr/bin/python


class Word:
    """Stats for a single word: how many times this word appears in a spam mail, and how many times it appears in a ham mail"""

    def __init__(self, spam_occurrences, ham_occurrences):
        """constructor"""
        self.ham_occurrences = ham_occurrences
        self.spam_occurrences = spam_occurrences
