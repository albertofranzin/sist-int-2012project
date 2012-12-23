import itertools
import os
import random

from bs4 import BeautifulSoup

from gen_stat import Stat
from test_stat import Test_stat


class Utils:
    """Collection of various tools used in the project."""

    @staticmethod
    def _read_files(path, how_many, read_mails,
            words, gen_stats, params):
        """
        Read the desidered number of text files from the given path.

        If desidered, extract first the text and then the tokens
        from the mails. Does nothing on the content of plain text files.

        :param path: the relative path from the current position\
           to the desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 == unlimited;
        :type how_many: int
        :param read_mails: tells if the user wants to read mails or plain text;
        :type read_mails: bool
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`gen_stat.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :param params: contains some general parameters and configurations;
        :type params: associative array
        :return: a list containing all the mails in the given files.

        """

        file_list = []
        print "path : ", os.getcwd()
        print "Utils :: _read_files :: ", path

        os.chdir(path)
        # runs through all the files
        list_of_files = os.listdir(".")
        # shuffle and choose some
        random.shuffle(list_of_files)
        if how_many > 0:
            del list_of_files[how_many:]

        for file in list_of_files:  # os.listdir("."):
            # open the file
            if params['VERBOSE']:
                print "Utils.read :: opening file", file  # , "\n\n"
            in_file = open(file, "r")
            # read all its content
            file_text = in_file.read()

            # Now, if it is explicitly requested to read mails, extract the
            # text content from the mail, get the tokens and extract stats.
            # Otherwise, append the plain text file
            if read_mails:
                soup = BeautifulSoup(''.join(file_text))
                file_list.append([soup.get_text()])
            else:
                file_list.append([file_text])

            # close file
            in_file.close()

        return file_list

    @staticmethod
    def read_mails(path, how_many, words, general_stats, params):
        """
        Read the desidered number of text files from the given path.

        Calls method Utils._read_files, passing the same parameters received,
        with `read_mails` flag set to True.

        :param path: the relative path from the current position to the \
                desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 == unlimited;
        :type how_many: int
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`gen_stat.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :param params: contains some general parameters and configurations;
        :type params: associative array
        :return: a list containing all the mails in the given files.

        """

        return Utils._read_files(path, how_many, True,
                words, general_stats, params)

    @staticmethod
    def read_text(path, how_many, params):
        """
        Read the desidered number of text files from the given path.

        Calls method Utils._read_files, passing the same parameters received,
        with `read_mails` flag set to False.

        :param path: the relative path from the current position \
                to the desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 = unlimited;
        :type how_many: int
        :param params: contains some general parameters and configurations;
        :type params: associative array
        :return: a list containing all the text in the given files.

        """

        return Utils._read_files(path, how_many, False, [], [], params)

    @staticmethod
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.

        From http://stackoverflow.com/questions/312443 (thanks).

        :param l: the list to be splitted;
        :type l: list of objects
        :param n: the size of the generated chunks.
        :type n: int

        """

        return [l[i: i + n] for i in range(0, len(l), n)]

    @staticmethod
    def merge_lists(lists):
        """Merge a list of lists into a single one.

        From http://stackoverflow.com/questions/406121 (thanks)

        :param lists: the list of lists to be flattened;
        :type lists: list
        :return: the new list.

        """

        chain = itertools.chain(*lists)
        return list(chain)

    @staticmethod
    def create_stats():
        """
        Defines a new associative array of (str, :class:`gen_stat.Stat`),
        containing all the overall stats to be evaluated by the Bayes network
        in the training step.

        :return: the newly created array.

        """

        gs = {}
        gs['ALLCAPSW']   = Stat("# of all-caps words", 0, 0)
        gs['ALPHANUM']   = Stat("# of alphanumerical words", 0, 0)
        gs['USERHOST']   = Stat("# of string in user/hosts form", 0, 0)
        gs['LINKADDR']   = Stat("# of links", 0, 0)
        gs['MAILADDR']   = Stat("# of mail addresses", 0, 0)
        gs['LOWERCASEW'] = Stat("# of all lowercase words", 0, 0)
        gs['TITLEW']     = Stat("# of words with only the first letter capital", 0, 0)
        gs['SHORTWORDS'] = Stat("# of \"short words\"", 0, 0)
        gs['LOONGWORDS'] = Stat("# of non-address \"very long words\"", 0, 0)
        gs['WASTE']      = Stat("# of non-valid words", 0, 0)
        gs['NUMBER']     = Stat("# of numbers", 0, 0)
        return gs

    @staticmethod
    def create_test_stats():
        """
        Defines a new associative array of (str, :class:`test_stat.Stat`),
        containing all the overall stats to be evaluated by the Bayes network
        in the validation and testing steps.

        :return: the newly created array.

        """

        gs = {}
        gs['ALLCAPSW']   = Test_stat("# of all-caps words", 0)
        gs['ALPHANUM']   = Test_stat("# of alphanumerical words", 0)
        gs['USERHOST']   = Test_stat("# of string in user/hosts form", 0)
        gs['LINKADDR']   = Test_stat("# of links", 0)
        gs['MAILADDR']   = Test_stat("# of mail addresses", 0)
        gs['LOWERCASEW'] = Test_stat("# of all lowercase words", 0)
        gs['TITLEW']     = Test_stat("# of words with only the first letter capital", 0)
        gs['SHORTWORDS'] = Test_stat("# of \"short words\"", 0)
        gs['LOONGWORDS'] = Test_stat("# of non-address \"very long words\"", 0)
        gs['WASTE']      = Test_stat("# of non-valid words", 0)
        gs['NUMBER']     = Test_stat("# of numbers", 0)
        return gs

    @staticmethod
    def create_file(file_name):
        """
        Creates an empty file.

        :param file_name: the name of the file to create.
        :type file_name: str

        """
        open(file_name, "w").close()
