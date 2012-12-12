class Stat:
    """
    Stats for mail characteristics: how many times this feature appears in
    a spam mail, and how many times it appears in a ham mail. Class used when
    training the network.

    """

    def __init__(self, description, words_spam, words_ham):
        """Constructor."""
        self.description = description
        self.spam = words_spam
        self.ham = words_ham


class Word:
    """
    Stats for a single word: how many times this word appears in a spam
    mail, and how many times it appears in a ham mail. Class used when
    training the network.

    """

    def __init__(self, spam_occurrences, ham_occurrences):
        """Constructor."""
        self.ham_occurrences = ham_occurrences
        self.spam_occurrences = spam_occurrences
