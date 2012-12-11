"""
.. module::naive_bayes
   :platform: Unix, Windows
   :synopsis: defines a Bayes network and its operations

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""

import locale
import math
import os
import sys

from classifier import Classifier
from config import Config
# from gen_stat import Stat
from lexer import Lexer
from trainer import Trainer
from utils import Utils


class Bayes():
    """
    Contains the Bayes network and some possible operations: training,
    validation, k-fold cross-validation, formatted print of the data.
    For the other operations, instantiate the apposite classes.

    """

    #
    # constructor
    #

    def __init__(self):
        """
        Constructor.

        Initialize all the objects and variables used to define a Bayes network:
        words stats, overall stats, configuration, trainer, validator.
        Saves the path of the project.

        """

        print "Bayes :: creating arrays"
        # associative array for the words and their occurrences
        self.words = {}
        # associative array for general stats of some interesting features of the mails
        self.general_stats = Utils.create_stats()
        print "Bayes :: arrays created"

        # lexer
        # print "Bayes :: tryin' to create the Lexer"
        # self.lexer = Lexer()
        # print "Bayes :: Lexer created"

        # config
        self.config = Config()
        print "Bayes :: Config created"

        print "Bayes :: tryin' to create the Trainer"
        self.trainer = Trainer()
        print "Bayes :: Trainer created"

        # set initial position of the project dir
        self.initial_path = os.getcwd()

    #
    # code for pretty-printing the results
    # slightly adapted from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/, many thanks
    #

    def bayes_print(self, print_words, print_gen_stats):
        """Prints out the data, padded for alignment.

        Slightly adapted from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/, many thanks.

        Each row must have the same number of columns.

        :param print_words: do I have to print the words retrieved?
        :type print_words: bool
        :param print_gen_stats: do I have to print the overall stats?
        :type print_gen_stats: bool

        """

        def _format_num(num):
            """Format a number according to given places.
            Adds commas, etc. Will truncate floats into ints!"""
            try:
                inum = int(num)
                return locale.format("%.*f", (0, inum), True)

            except (ValueError, TypeError):
                return str(num)

        def _get_max_width(table, index):
            """Get the maximum width of the given column index"""
            return max([len(_format_num(row[index])) for row in table])

        def _pprint_table(out, table):
            """formats and prints the given table"""
            col_paddings = []
            firstrow = True
            ll = []

            for i in range(len(table[0])):
                col_paddings.append(_get_max_width(table, i))

            for row in table:
                # left col
                print >> out, row[0].ljust(col_paddings[0] + 2),
                if firstrow:
                    ll.append(len(row[0].ljust(col_paddings[0] + 1)) + 1)
                # rest of the cols
                for i in range(1, len(row)):
                    col = _format_num(row[i]).rjust(col_paddings[i] + 2)
                    if firstrow:
                        ll.append(len(col))
                    print >> out, " | ", col,
                print >> out
                if firstrow:
                    print >> out, '-' * ll[0],
                    for i in range(1, len(ll)):
                        print >> out, ' | ', '-' * ll[i],
                    print >> out
                    firstrow = False

        # Now create the tables and print'em.
        # For both the words and the overall stats:
        # creates the printable table, each row is a stat.
        # The first row has the table header.

        locale.setlocale(locale.LC_NUMERIC, "")
        out = sys.stdout

        if print_words:
            table = [['word', 'spam', 'ham']]
            for item in print_words.iterkeys():
                table.append([item, print_words[item].spam_occurrences,
                                    print_words[item].ham_occurrences])

            print "\nWords:"
            _pprint_table(out, table)

        if print_gen_stats:
            table = [['Feature description',
                      '# occurrences in spam mails',
                      '# occurrences in ham mails']]

            for item in print_gen_stats.itervalues():
                table.append([item.description, item.spam, item.ham])

            print "\nResults:"

            _pprint_table(out, table)

    #
    # cross-validation
    #

    def _k_fold_cross_validation(self, spam_list, ham_list):
        """Internal method, execute the k-fold cross-validation TODO: FINISH

        Splits the lists in the desidered number of parts
        (see :class:`config.Config` object),
        then calls the :func:`trainer.Trainer.train()` function.

        :param spam_list: the list of spam mails to be used;
        :type spam_list: array of str
        :param ham_list: the list of ham mails to be used;
        :type ham_list: array of str
        :return: the accuracy of the training.

        """

        folds     = self.config.CROSS_VALIDATION_FOLDS
        fold_size = int(math.ceil(self.config.SIZE_OF_BAGS / folds))
        accuracy = []

        spam_chunks = Utils.chunks(spam_list, fold_size)
        ham_chunks  = Utils.chunks(ham_list, fold_size)

        for iteration in range(0, folds):
            spam_kfold_train = []
            ham_kfold_train  = []
            spam_kfold_valid = spam_chunks[iteration]
            ham_kfold_valid  = ham_chunks[iteration]
            for it in range(0, folds):
                if it != iteration:
                    spam_kfold_train.append(spam_chunks[it])
                    ham_kfold_train.append(ham_chunks[it])
                ws = {}
                gs = Utils.create_stats()
                Trainer.train(ws, gs, self.config)
                accuracy.append(Trainer.tr)

        return 0.5

    #
    # train
    #

    def train(self):
        """
        Train the net. TODO: COMPLETE CROSS-VALIDATION

        Read the mails given as training and validation set for spam and ham,
        then executes the proper training. Two methods are available: the direct
        training, and the k-fold cross-validation.

        First of all, read the training set and validation set mails.
        If the k-fold cross-validation is chosen (see :class:`config.Config`
        documentation), then call the apposite method, otherwise calls the
        :class:`trainer.Trainer` object to extract from the training set
        the feature stats, then compute the accuracy by calling the
        :func:`naive_bayes.Bayes.validate` object, to find out the goodness of
        the classification.

        No parameters are needed, since everything the network needs is already
        present. The location of the mails is (for now?) hardcoded here.

        """

        if self.config.VERBOSE:
            print "Bayes :: train :: traning begins"

        # read training+validation ham mails together, then split the two sets.
        if self.config.VERBOSE:
            print "Bayes :: train :: begin to read ham"
        path = "./spam/ham/"
        ham_list = Utils.read_mails(path,
            self.config.SIZE_OF_BAGS + self.config.SIZE_OF_VAL_BAGS,
            self.words, self.general_stats, self.config)
        [ham_list, ham_val_list] = Utils.chunks(ham_list, self.config.SIZE_OF_BAGS)

        # read training+validation ham mails together, then split the two sets.
        if self.config.VERBOSE:
            print "Bayes :: train :: begin to read spam"
        path = "../spam/"
        spam_list = Utils.read_mails(path,
            self.config.SIZE_OF_BAGS + self.config.SIZE_OF_VAL_BAGS,
            self.words, self.general_stats, self.config)
        [spam_list, spam_val_list] = Utils.chunks(spam_list, self.config.SIZE_OF_BAGS)

        # is cross-validation the chosen option?
        if self.config.CROSS_VALIDATION:
            # call cross-validation function
            pass
        else:
            # train directly
            self.trainer.train(spam_list, True,
                    self.words, self.general_stats, self.config)
            self.trainer.train(ham_list, False,
                    self.words, self.general_stats, self.config)

            if self.config.VERBOSE:
                self.trainer.trainer_print(self.general_stats)

            # call normal validation function
            accuracy = self.validate(ham_val_list, spam_val_list,
                self.words, self.general_stats, self.config)

            if self.config.VERBOSE:
                print "Bayes :: accuracy of the trained network: ", accuracy

    #
    # validation
    #

    def validate(self, ham_val_list, spam_val_list,
            words, general_stats, config):
        """
        Validation function.

        Get the validation sets and the results of the training, and
        compute the accuracy of the classification of the mails
        in the validation set.

        :param ham_val_list: the good mails of the validation set;
        :type ham_val_list: array of mails
        :param spam_val_list: the spam mails of the validation set;
        :type spam_val_list: array of mails
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`word.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :param config: contains some general parameters and configurations;
        :type config: :class:`config.Config` object
        :return: accuracy of the validation.

        """

        size = config.SIZE_OF_VAL_BAGS
        size += 1
        ws = {}
        gs = Utils.create_stats()
        lexer = Lexer()

        for mail in ham_val_list:
            lexer.lexer_words(mail, True, ws, gs, config)
            # classify as spam/ham?

        return 0

    #
    # test
    #

    def test_bayes(self):
        """Performs some test - needed to try some functions."""

        mws = {}
        mgs = Utils.create_stats()

        print "Bayes :: test_bayes :: reading the mails"
        boh_list = Utils.read_mails(self.initial_path + "/spam/mine/",
                3, mws, mgs, self.config)

        print "Bayes :: test_bayes :: going to train"
        self.trainer.train(boh_list, True, mws, mgs, self.config)
        # self.bayes_print(mws, mgs)

        print "Bayes :: test_bayes :: going to test the classifier"
        Classifier.classify(mws, mgs, self.words, self.general_stats, self.config)

        raw_input('\nMay I go on? ')

        print "Bayes :: test_bayes :: now try some ham"
        mws = {}
        mgs = Utils.create_stats()
        boh_list = Utils.read_mails(self.initial_path + "/spam/mine/ham/",
                1, mws, mgs, self.config)
        self.trainer.train(boh_list, False, mws, mgs, self.config)
        self.bayes_print(mws, mgs)

        print "Bayes :: test_bayes :: going to test the classifier"
        Classifier.classify(mws, mgs, self.words, self.general_stats, self.config)
