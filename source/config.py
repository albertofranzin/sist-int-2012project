class Config():
    """Set some configurations"""

    def __init__(self):
        """constructor"""

        # some constants:

        # length of a token to be defined "a short word"
        self.SHORT_THR = 1

        # length of a token to be defined "a very long word"
        self.VERYLONG_THR = 20

        # size of training sets
        self.SIZE_OF_BAGS = 50
