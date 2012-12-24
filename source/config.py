import ConfigParser


class Config():
    """
    Contains some general configurations. After the parameter array is created,
    read the config file (`spam_bayes.conf`) to overwrite the settings
    desidered by the user.

    The available parameters are (with `[default]` values):

    - CROSS_VALIDATION (bool): True if k-fold cross-validation is chosen.\
        False otherwise [False];
    - CROSS_VALIDATION_FOLDS (int): the number of folds for\
        cross-validation, if enabled [4];
    - OVERALL_FEATS_SPAM_W (float, in [0,1]): the weight of the overall stats\
        when computing the spamicity of a mail. The remaining part is given by\
        the word stats [0.0001];

    - READ_FROM_FILE (bool): True if the network has to load some previous\
        result, False if training has to be done from scratch [False];
    - INPUT_ID (str): relative path to the files that have to be read, with the\
        prefix of the file names (see :func:`naive_bayes.Bayes.read_bayes()`)\
        [saved_runs/saved_network];
    - PARAMS_FROM_FILE (bool): True if also the parameters have to be loaded from file,\
        False if the current parameters are preferres. Better to be specified,\
        since different parameters lead to different results [True] ;

    - RELEVANCE_THR (float, in [0,0.5]): specifies how much relevant a word or\
        a feature has to be to be considered in the spamicity computation; that is,\
        how much it differs from 1/2, to spam or ham. Useful to exclude negligible\
        words or features (the ones that appear in spam mails as much as they do in\
            ham ones) [0.25];
    - SHORT_THR (int): length of a word to be identified as `very short` [1];
    - SIZE_OF_BAGS (int): number of ham and spam mails for training [800];
    - SIZE_OF_VAL_BAGS (int): number of ham and spam mails for validation [200];
    - SIZE_OF_TEST_BAG (int): number of mails in the test set [1000]
    - SMOOTH_VALUE (float): smoothing value to be used in classification [0.001];
    - SPAM_THR (float, \in [0,1]): probability threshold to mark a mail as spam [0.2];
    - ADAPTIVE_SPAM_THR (bool): True if the `SPAM_THR` value has to be tuned according\
        to the results of the classification of the mails, False if the threshold\
        must be the same from the beginning to the end [True];
    - VERBOSE (bool): if True, displays more messages, if False, display only some\
        necessary messages [False];
    - VERYLONG_THR (int): length of a word to be identified as `very long` [18];

    - SPAM_DIR (str): the relative path from the project dir to the directory\
        containing the spam mails [spam/spam/];
    - HAM_DIR (str): the relative path from the project dir to the directory\
        containing the ham mails [spam/ham/];

    - WRITE_TO_FILE (bool): True if the network has to writethe computed\
        result, False if not [True];
    - OUTPUT_ID (str): relative path to the files that have to be written, with the\
        prefix of the file names (see :func:`naive_bayes.Bayes.write_bayes()`)\
        [saved_runs/saved_network].

    """

    def __init__(self):
        """
        Constructor. Initialize all the parameters to their default value,
        then check for different choices by the user, reading the file
        `spam_bayes.conf`.

        """

        # define the constants
        self.params = {}

        # do I have to do cross-validation? [False]
        self.params['CROSS_VALIDATION'] = False

        # # of cross-validation folds (if enabled) [4]
        self.params['CROSS_VALIDATION_FOLDS'] = 4

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

        # threshold of deviance of a statistic from the average mean [0.25]
        self.params['RELEVANCE_THR'] = 0.25

        # length of a token to be defined "a short word" [1]
        self.params['SHORT_THR'] = 1

        # size of training sets [800]
        self.params['SIZE_OF_BAGS'] = 800

        # size of validation sets (1 v.s. for ham, 1 for spam) [200]
        self.params['SIZE_OF_VAL_BAGS'] = 200

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

        # should the SPAM_THR threshold be adapted looking at the results? [True]
        self.params['ADAPTIVE_SPAM_THR'] = True

        # should I print lots of infos? [False]
        self.params['VERBOSE'] = False

        # length of a token to be defined "a very long word" [18]
        self.params['VERYLONG_THR'] = 18

        # do I have to write on hard drive the stats computed? [True]
        self.params['WRITE_TO_FILE'] = True

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

        :return: the parameter list.

        """

        return self.params
