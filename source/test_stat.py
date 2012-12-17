class Test_stat:
    """
    Stats for a single mail belonging to the test set or to
    the validation set. So, it it not possible, at the stage this object
    is created, to tell whether the mail is spam or ham. Class used when
    validating and testing the network.

    """

    def __init__(self, description, count):
        """Constructor. Initialize the stat."""
        self.description = description
        self.count = count


class Test_word:
    """
    Stats for a single word: how many times this word appears in the parsed
    mail. Class used when validating and testing the network. It is probably
    useless, but it keeps some "simmetry" with the one used in training.

    """

    def __init__(self, occurrences):
        """Constructor."""
        self.occurrences = occurrences
