import ConfigParser

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
    - SIZE_OF_TEST_BAG (int): number of mails in the test set [30]
    - SMOOTH_VALUE (int): smoothing value to be used in classification [1];
    - SPAM_THR (float, \in [0,1]): probability threshold to mark a mail as spam [0.95];
    - VERBOSE (bool): if True, displays more messages [True];
    - VERYLONG_THR (int): length of a word to be identified as `very long` [20].

    """

    def __init__(self):
        """
        Constructor. Initialize all the parameters to their default value.

	If found in file config.cfg, initialize to that value.

        """

        # some constants:
	self.params = {}

        # do I have to do cross-validation?
        self.params['CROSS_VALIDATION'] = False

        # # of cross-validation folds (if enabled)
        self.params['CROSS_VALIDATION_FOLDS'] = 4

        # weight of the overall features stats over the word spamminess
        self.params['OVERALL_FEATS_SPAM_W'] = 0.6

        # length of a token to be defined "a short word"
        self.params['SHORT_THR'] = 1

        # size of training sets
        self.params['SIZE_OF_BAGS'] = 50

        # size of validation sets
        # (1 v.s. for ham, 1 for spam)
        # MUST BE <= SIZE_OF_BAGS
        self.params['SIZE_OF_VAL_BAGS'] = 50

        # size of test set
        self.params['SIZE_OF_TEST_BAG'] = 30

        # smooth value
        self.params['SMOOTH_VALUE'] = 1

        # spam probability threshold for classification and validation
        self.params['SPAM_THR'] = 0.5

        # should I print lots of infos?
        self.params['VERBOSE'] = False

        # length of a token to be defined "a very long word"
        self.params['VERYLONG_THR'] = 20


        # Reading values from config.cfg

        config = ConfigParser.RawConfigParser()

        config.read('config.cfg')

        for (param,value) in self.params.items():
            try:
                x = config.get('Main', param)
                self.params[param] = x
            except ConfigParser.NoOptionError:
                #print "Missing",param,"parameter, keeping default"

    def cprint(self):
        """ Cprint. Print all the parameters and their assigned value """

        param_list=self.params.keys()
        for param in param_list:
		print param,"set to",self.params[param]

