"""
.. module::naive_bayes
   :platform: Unix, Windows
   :synopsis: defines a Bayes network and its operations

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""
from __future__ import division

import csv
import locale
import math
import os
import random
import sys

from classifier import Classifier
from config import Config
from gen_stat import Stat, Word
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

        print "Bayes :: initialize all"
        # associative array for the words and their occurrences
        self.words = {}
        # associative array for general stats of some interesting features of the mails
        self.general_stats = Utils.create_stats()

        # lexer
        # print "Bayes :: tryin' to create the Lexer"
        # self.lexer = Lexer()
        # print "Bayes :: Lexer created"

        # config
        self.config = Config()
        self.params = self.config.get_params()
        print "Bayes :: Config created"

        print "Bayes :: tryin' to create the Trainer"
        self.trainer = Trainer()
        print "Bayes :: Trainer created"

        # set initial position of the project dir
        self.initial_path = os.getcwd()

        # other variables
        self.false_positives = 0.0
        self.false_negatives = 0.0

        # the lists of mails
        self.ham_list       = []
        self.spam_list      = []
        self.ham_val_list   = []
        self.ham_test_list  = []
        self.spam_val_list  = []
        self.spam_test_list = []

        print "Bayes :: done"

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

        folds     = self.params['CROSS_VALIDATION_FOLDS']
        fold_size = int(math.ceil(self.params['SIZE_OF_BAGS'] / folds))
        acc_array = []

        spam_chunks = Utils.chunks(spam_list, fold_size)
        ham_chunks  = Utils.chunks(ham_list, fold_size)

        # print spam_list

        # raw_input("got it?")

        for iteration in range(0, folds):
            # for every iteration, join up the training set chunks, leaving out
            # each time only one chunk.
            # The chunk left out will be the validation set.
            spam_kfold_train = []
            spam_kfold_valid = []
            ham_kfold_train  = []
            ham_kfold_valid  = []

            for it in range(0, folds):
                if it != iteration:
                    spam_kfold_train.append(spam_chunks[it])
                    ham_kfold_train.append(ham_chunks[it])
                else:
                    spam_kfold_valid.append(spam_chunks[it])
                    ham_kfold_valid.append(ham_chunks[it])

            wos = {}
            gos = Utils.create_stats()

            spam_kfold_train = Utils.merge_lists(spam_kfold_train)
            spam_kfold_valid = Utils.merge_lists(spam_kfold_valid)
            ham_kfold_train  = Utils.merge_lists(ham_kfold_train)
            ham_kfold_valid  = Utils.merge_lists(ham_kfold_valid)
            print len(spam_kfold_train), len(spam_kfold_valid),
            print len(ham_kfold_train), len(ham_kfold_valid)
            # raw_input("mah na mah na")

            self.trainer.train(spam_kfold_train, True, wos, gos, self.params)
            self.trainer.train(ham_kfold_train, False, wos, gos, self.params)
            # self.bayes_print(wos, gos)
            # raw_input("mah na mah na")

            # if self.params['VERBOSE']:
            #     self.trainer.trainer_print(gos)
            #     self.bayes_print(wos, gos)

            acc_array.append(self.validate(ham_kfold_valid, spam_kfold_valid,
                wos, gos))

            # update the stats of the Naive Bayes network
            # self.update_training_stats()

            # raw_input("ok, ok")

        # compute the median of the accuracies, which will be the final accuracy
        # obtained with the k-fold cross validation
        print "KFOLD-CROSS-VALIDATION :: ", acc_array,
        acc_array = sorted(acc_array)
        alen = len(acc_array)
        accuracy = 0.5 * (acc_array[(alen - 1) // 2] + acc_array[alen // 2])
        print accuracy

        return accuracy

    #
    # train
    #

    def train(self):
        """
        Train the net.

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

        Mails are expected to be found in the directories given when filling in
        the `spam_bayes.conf` file.

        """

        if self.params['VERBOSE']:
            print "Bayes :: train :: training begins"

        self.load_mails()

        # is cross-validation the chosen option?
        if self.params['CROSS_VALIDATION']:
            self._k_fold_cross_validation(self.spam_list, self.ham_list)

        # raw_input("training HAM")
        self.trainer.train(self.ham_list, False,
                self.words, self.general_stats, self.params)
        # raw_input("training SPAM")
        self.trainer.train(self.spam_list, True,
                self.words, self.general_stats, self.params)

        #if self.params['VERBOSE']:
        self.trainer.trainer_print(self.general_stats)
        # self.bayes_print(self.words, self.general_stats)

    #
    # check (validation & testing)
    #

    def check(self):
        """
        Compute accuracies for validation and testing.

        """

        # call method for validation
        accuracy = self.validate(self.ham_val_list, self.spam_val_list,
            self.words, self.general_stats)

        print "Bayes :: accuracy of the trained network: ", accuracy

        # call same method of above for testing
        accuracy = self.validate(self.ham_test_list, self.spam_test_list,
            self.words, self.general_stats)

        print "Bayes :: accuracy with test set: ", accuracy

    #
    # validation
    #

    def validate(self, ham_list, spam_list, words, general_stats):
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
        :type words: array of :class:`gen_stat.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :return: accuracy of the validation.

        """

        # Mails are shuffled, so updating the stats can bring some result...
        print len(ham_list), len(spam_list)
        total_list = ham_list + spam_list
        random.shuffle(total_list)

        count = 0
        lexer = Lexer()
        # false_positives = 0
        # false_negatives = 0

        # for mail_couple in total_list:
        for [mail, status] in total_list:
            print status, " :: ",
            ws = {}
            gs = Utils.create_test_stats()
            lexer.lexer_words(mail, False, False, ws, gs, self.params)
            res = Classifier.classify(ws, gs, words, general_stats, self.params)
            # has the mail been classified correctly?
            if res == status:
                # yes
                count += 1
                print " :: correct!"
                # self.update_stats(ws, gs, status)
            else:
                # no
                if res == True:
                    self.false_positives += 1
                    print " :: wrong! so far we have", self.false_positives,\
                            "false positives",
                    self.params['SPAM_THR'] = math.fabs(self.params['SPAM_THR'] +
                            0.1 / (self.false_negatives + 1))
                    print self.params['SPAM_THR']
                else:
                    self.false_negatives += 1
                    print " :: wrong! so far we have", self.false_negatives,\
                            "false negatives",
                    self.params['SPAM_THR'] = math.fabs(self.params['SPAM_THR'] -
                            0.1 / (self.false_positives + 1))
                    print self.params['SPAM_THR']
            self.update_stats(ws, gs, res)  # status

        print "false pos:", self.false_positives, "false neg:", self.false_negatives

        return count / (len(ham_list) + len(spam_list))

    #
    # test
    #

    def test_bayes(self):
        """Performs some test - needed to try some functions."""
        pass

    #
    # update the stats
    #

    def update_stats(self, ws, gs, is_spam):
        """
        Update the overall stats, using the stats computed for a single mail
        and its status.

        :param ws: the list of words found in the mail;
        :type ws: array of :class:`test_stat.Test_word`
        :param gs: the list of features found in the mail;
        :type gs: array of :class:`test_stat.Test_stat`
        :param is_spam: `True` if the mail is spam, `False` otherwise.
        :type is_spam: bool

        """

        if is_spam:
            for word in ws.keys():
                count = ws[word].occurrences
                if word in self.words:
                    self.words[word].spam_occurrences += count
                else:
                    self.words[word] = Word(count, 0)
        else:
            for word in ws.keys():
                count = ws[word].occurrences
                if word in self.words:
                    self.words[word].ham_occurrences += count
                else:
                    self.words[word] = Word(0, count)

        if is_spam:
            for stat_id in gs.keys():
                self.general_stats[stat_id].spam += gs[stat_id].count
        else:
            for stat_id in gs.keys():
                self.general_stats[stat_id].ham += gs[stat_id].count

    #
    # write stats&params on file
    #

    def write_bayes(self):
        """
        Write the overall stats computed to file.

        Three files will be created:

        1. `ID_words.csv`, containing the stats of the words;
        2. `ID_feats.csv`, containing the stats of the features;
        3. `ID_params.csv`, containing the configuration used,

        where `ID` is the value contained in `params['OUTPUT_ID']`.

        """

        w_file = self.params['OUTPUT_ID'] + '_words.csv'
        f_file = self.params['OUTPUT_ID'] + '_feats.csv'
        p_file = self.params['OUTPUT_ID'] + '_params.csv'

        if self.params['VERBOSE']:
            print "Bayes :: write_bayes :: creating ", w_file, f_file, p_file

        os.chdir(self.initial_path)
        Utils.create_file(w_file)
        Utils.create_file(f_file)
        Utils.create_file(p_file)

        # can't put all of this in Utils since I don't know how to save
        # an entire object... don't know Python so well, sorry

        # print the stats of the words
        if self.params['VERBOSE']:
            print "Bayes :: write_bayes :: writing file", w_file, "...",

        with open(w_file, 'w') as csvfile:
            writer = csv.writer(csvfile,
                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for (word, stat) in self.words.items():
                writer.writerow([word, stat.spam_occurrences, stat.ham_occurrences])

        if self.params['VERBOSE']:
            print "done"

        # print the stats of the features
        if self.params['VERBOSE']:
            print "Bayes :: write_bayes :: writing file", f_file, "..."

        with open(f_file, 'w') as csvfile:
            writer = csv.writer(csvfile,
                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for (feat, stat) in self.general_stats.items():
                writer.writerow([feat, stat.description, stat.spam, stat.ham])

        if self.params['VERBOSE']:
            print "done"

        # print the params
        if self.params['VERBOSE']:
            print "Bayes :: write_bayes :: writing file", p_file, "..."

        with open(p_file, 'w') as csvfile:
            writer = csv.writer(csvfile,
                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for (param, value) in self.params.items():
                writer.writerow([param, value])

        if self.params['VERBOSE']:
            print "done"

    #
    # read from files
    #

    def read_bayes(self):
        """
        Read the overall stats computed in a previous run from files, and then
        load validation and test set, since the training step won't be launched.

        Three files are expected to be found:

        1. `ID_words.csv`, containing the stats of the words;
        2. `ID_feats.csv`, containing the stats of the features;
        3. `ID_params.csv`, containing the configuration used,

        where `ID` is the value contained in `params['INPUT_ID']`.

        Validation and test sets are loaded from the same place they are
        expected to be when training "normally".

        """

        # can't put all of this in Utils since I don't know how to read
        # an entire object... don't know Python so well, sorry

        w_file = self.params['INPUT_ID'] + '_words.csv'
        f_file = self.params['INPUT_ID'] + '_feats.csv'
        p_file = self.params['INPUT_ID'] + '_params.csv'

        if self.params['VERBOSE']:
            print "Bayes :: read_bayes :: opening", w_file, f_file, p_file

        # read the stats of the words
        if self.params['VERBOSE']:
            print "Bayes :: read_bayes :: reading file", f_file, "..."

        with open(w_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for [word, s_occ, h_occ] in reader:
                self.words[word] = Word(int(s_occ), int(h_occ))

        if self.params['VERBOSE']:
            print "done"

        # read the stats of the features
        if self.params['VERBOSE']:
            print "Bayes :: read_bayes :: reading file", f_file, "..."

        with open(f_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for [feat, description, spam, ham] in reader:
                self.general_stats[feat] = Stat(description, int(spam), int(ham))

        if self.params['VERBOSE']:
            print "done"

        if self.params['PARAMS_FROM_FILE']:
            # read the params
            if self.params['VERBOSE']:
                print "Bayes :: read_bayes :: reading file", p_file, "..."

            with open(p_file, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for [param, value] in reader:

                    # check it param is an integer
                    try:
                        self.params[param] = int(value)
                        continue
                    except ValueError:
                        pass

                    # check if param is a float
                    try:
                        self.params[param] = float(value)
                        continue
                    except ValueError:
                        pass

                    # check if param is a boolean
                    # quick 'n' dirty, don't know if there is
                    # a more straightforward way
                    try:
                        # self.params[param] = bool(user_value)
                        if value == "True":
                            self.params[param] = True
                            continue
                        elif value == "False":
                            self.params[param] = False
                            continue
                    except ValueError:
                        pass

                    # finally, if it's nothing else, then it's a string
                    self.params[param] = value

            if self.params['VERBOSE']:
                print "done"
                self.config.cprint()

        self.load_mails()

    #
    # load the dataset
    #

    def load_mails(self):
        """
        Read the desidered number of mails and group them in the three sets.

        """

        # read training+validation+test ham mails together,
        # then split the three sets.
        if self.params['VERBOSE']:
            print "Bayes :: load_mails :: begin to read ham"

        # for not knowing how to read or write (do they say this in English? Mah...)
        # reset the path to the project folder
        os.chdir(self.initial_path)

        # read all the ham
        total_ham_list = Utils.read_mails(self.params['HAM_DIR'],
            self.params['SIZE_OF_BAGS'] + self.params['SIZE_OF_VAL_BAGS'] +\
                    self.params['SIZE_OF_TEST_BAGS'],
            self.words, self.general_stats, self.params)

        # split the three sets
        # training ham can stay like it is
        # validation and testing will be shuffled, so each mail has to be
        # paired with its status, to be able to check later
        self.ham_list = total_ham_list[0:self.params['SIZE_OF_BAGS']]
        ham_val_list_tmp = total_ham_list[self.params['SIZE_OF_BAGS']:\
                self.params['SIZE_OF_BAGS'] + self.params['SIZE_OF_VAL_BAGS']]
        ham_test_list_tmp = total_ham_list[self.params['SIZE_OF_BAGS'] +\
                self.params['SIZE_OF_VAL_BAGS']:]

        for item in ham_val_list_tmp:
            self.ham_val_list.append([item, False])
        for item in ham_test_list_tmp:
            self.ham_test_list.append([item, False])

        del total_ham_list, ham_val_list_tmp, ham_test_list_tmp

        # now, go with spam
        # read training+validation+test ham mails together,
        # then split the three sets.
        if self.params['VERBOSE']:
            print "Bayes :: train :: begin to read spam"

        # Houston, we need a reset
        os.chdir(self.initial_path)

        # read all the spam
        total_spam_list = Utils.read_mails(self.params['SPAM_DIR'],
            self.params['SIZE_OF_BAGS'] + self.params['SIZE_OF_VAL_BAGS'] +\
                    self.params['SIZE_OF_TEST_BAGS'],
            self.words, self.general_stats, self.params)

        # split the three sets
        # training spam can stay like it is
        # validation and testing will be shuffled, so each mail has to be
        # paired with its status, to be able to check later
        self.spam_list = total_spam_list[0:self.params['SIZE_OF_BAGS']]
        spam_val_list_tmp = total_spam_list[self.params['SIZE_OF_BAGS']:\
                self.params['SIZE_OF_BAGS'] + self.params['SIZE_OF_VAL_BAGS']]
        spam_test_list_tmp = total_spam_list[self.params['SIZE_OF_BAGS'] +\
                self.params['SIZE_OF_VAL_BAGS']:]

        for item in spam_val_list_tmp:
            self.spam_val_list.append([item, True])
        for item in spam_test_list_tmp:
            self.spam_test_list.append([item, True])

        del total_spam_list, spam_val_list_tmp, spam_test_list_tmp

        # finally, reset path once again
        os.chdir(self.initial_path)
