#!/usr/bin/python


class Stat:
    "Stats for mail characteristics: how many times this feature appears in a spam mail, and how many times it appears in a ham mail"
    def __init__(self, description, words_spam, words_ham):
        self.description = description
        self.spam = words_spam
        self.ham = words_ham
