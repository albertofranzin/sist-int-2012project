class Config():
    """
    Contains some general configurations.

    The available parameters are (with `[default]` values):

    - CROSS_VALIDATION (bool): True if k-fold cross-validation is chosen.\
        False otherwise [True];
    - CROSS_VALIDATION_FOLDS (int): the number of folds for\
        cross-validation, if enabled [4];
    - OVERALL_FEATS_SPAM_W (float, \in [0,1]): the weight of the overall stats\
        when computing the spamicity of a mail. The remaining part is given by\
        the word stats [0.7];
    - SHORT_THR (int): length of a word to be identified as `very short` [1];
    - SIZE_OF_BAGS (int): number of ham and spam mails for training [50];
    - SIZE_OF_VAL_BAGS (int): number of ham and spam mails for validation [10];
    - SMOOTH_VALUE (int): smoothing value to be used in classification [1];
    - SPAM_THR (float, \in [0,1]): probability threshold to mark a mail as spam [0.95];
    - VERBOSE (bool): if True, displays more messages [True];
    - VERYLONG_THR (int): length of a word to be identified as `very long` [20].

    """

    def __init__(self):
        """Constructor. Initialize all the parameters to their default value."""

        # some constants:

        # do I have to do cross-validation?
        self.CROSS_VALIDATION = False

        # # of cross-validation folds (if enabled)
        self.CROSS_VALIDATION_FOLDS = 4

        # weight of the overall features stats over the word spamminess
        self.OVERALL_FEATS_SPAM_W = 0.7

        # length of a token to be defined "a short word"
        self.SHORT_THR = 1

        # size of training sets
        self.SIZE_OF_BAGS = 50

        # size of validation sets
        # (1 v.s. for ham, 1 for spam)
        self.SIZE_OF_VAL_BAGS = 10

        # smooth value
        self.SMOOTH_VALUE = 1

        # spam probability threshold for classification and validation
        self.SPAM_THR = 0.95

        # should I print lots of infos?
        self.VERBOSE = True

        # length of a token to be defined "a very long word"
        self.VERYLONG_THR = 20
