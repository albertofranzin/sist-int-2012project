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
        """Constructor. Initialize all the parameters to their default value."""

        # define the constants
        self.params = {}

        # do I have to do cross-validation? [False]
        self.params['CROSS_VALIDATION'] = False

        # # of cross-validation folds (if enabled) [4]
        self.params['CROSS_VALIDATION_FOLDS'] = 8

        # weight of the overall features stats over the word spamminess [0.0001]
        self.params['OVERALL_FEATS_SPAM_W'] = 0.0001

        # do I have to read stats already computed? [False]
        self.params['READ_FROM_FILE'] = False

        # if yes, which file? [saved_network]
        # NOTE: ONLY THE FIRST PART OF THE FILE NAMES, TO IDENTIFY THE SESSION
        self.params['INPUT_ID'] = "saved_runs/saved_network"

        # should I use the params read from a file? [True]
        # only to be used if READ_FROM_FILE = True
        self.params['PARAMS_FROM_FILE'] = True

        # threshold of deviance of a statistic from the average mean
        self.params['RELEVANCE_THR'] = 0.15

        # length of a token to be defined "a short word" [1]
        self.params['SHORT_THR'] = 1

        # size of training sets [50]
        self.params['SIZE_OF_BAGS'] = 50

        # size of validation sets (1 v.s. for ham, 1 for spam) [50]
        self.params['SIZE_OF_VAL_BAGS'] = 50

        # size of test set [1000]
        self.params['SIZE_OF_TEST_BAGS'] = 1000

        # smooth value [0]
        self.params['SMOOTH_VALUE'] = 0.001

        # location of the spam folder ["./spam/spam/"]
        # (relative path from the project folder)
        self.params['SPAM_DIR'] = "./spam/spam/"

        # location of the ham folder ["./spam/ham/"]
        # (relative path from the project folder)
        self.params['HAM_DIR'] = "./spam/ham/"

        # spam probability threshold for classification and validation [0.2]
        self.params['SPAM_THR'] = 0.2

        # should I print lots of infos? [False]
        self.params['VERBOSE'] = False

        # length of a token to be defined "a very long word" [20]
        self.params['VERYLONG_THR'] = 18

        # do I have to write on hard drive the stats computed? [True]
        self.params['WRITE_ON_FILE'] = True

        # if yes, which file? [saved_runs/saved_network]
        # NOTE: ONLY THE FIRST PART OF THE FILE NAMES, TO IDENTIFY THE SESSION
        self.params['OUTPUT_ID'] = "saved_runs/saved_network"

        # Read values from file spam_bayes.conf, and
        # overwrite the default values

        config_parser = ConfigParser.RawConfigParser()

        config_parser.read('spam_bayes.conf')

        for (param, value) in self.params.items():
            try:
                user_value = config_parser.get('Main', param)

                # check it param is an integer
                try:
                    self.params[param] = int(user_value)
                    continue
                except ValueError:
                    pass

                # check if param is a float
                try:
                    self.params[param] = float(user_value)
                    continue
                except ValueError:
                    pass

                # check if param is a boolean
                # quick 'n' dirty, don't know if there is
                # a more straightforward way
                try:
                    # self.params[param] = bool(user_value)
                    if user_value == "True":
                        self.params[param] = True
                        continue
                    elif user_value == "False":
                        self.params[param] = False
                        continue
                except ValueError:
                    pass

                # finally, if it's nothing else, then it's a string
                self.params[param] = user_value
            except ConfigParser.NoOptionError:
                # print "Missing", param, "parameter, keeping default"
                pass

        if self.params['VERBOSE']:
            self.cprint()

    def cprint(self):
        """
        Print all the parameters and their assigned value.

        """

        print "Parameters:"
        param_list = self.params.keys()
        for param in param_list:
                print param, "set to", self.params[param]

    def get_params(self):
        """
        Return the parameter list.

        """

        return self.params
