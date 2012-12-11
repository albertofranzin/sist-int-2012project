import os

from bs4 import BeautifulSoup

from gen_stat import Stat
# from lexer import Lexer


class Utils:
    """Collection of various tools used in the project."""

    @staticmethod
    def _read_files(path, how_many, read_mails,
            words, gen_stats, config):
        """
        Read the desidered number of text files from the given path.

        If desidered, extract first the text and then the tokens
        from the mails. Does nothing on the content of plain text files.

        :param path: the relative path from the current position
        to the desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 == unlimited;
        :type how_many: int
        :param read_mails: tells if the user wants to read mails or plain text;
        :type read_mails: bool
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`word.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :param config: contains some general parameters and configurations;
        :type config: :class:`config.Config` object
        :return: a list containing all the mails in the given files.

        """

        # if we don't want to use the entire mail archive for train the system,
        # then we have to keep track of how many mails we have opened
        if how_many > 0:
            processed_mails = 0

        # # if we went to read mails, then we create the lexer to extract tokens
        # if read_mails:
        #     lexer = Lexer()

        file_list = []
        print "Utils :: _read_files :: ", path
        os.chdir(path)
        # runs through all the files
        for file in os.listdir("."):
            # open the file
            if config.VERBOSE:
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
                # lexer.lexer_words(soup.get_text(), True,
                #     words, gen_stats, config)
            else:
                file_list.append([file_text])
            # close file
            in_file.close()

            # keep the count of read mails if needed, and stop when done
            if how_many > 0:
                processed_mails += 1
                if processed_mails >= how_many:
                    processed_mails = 0
                    break

        return file_list

    @staticmethod
    def read_mails(path, how_many, words, general_stats, config):
        """
        Read the desidered number of text files from the given path.

        Calls method Utils._read_files, passing the same parameters received,
        with `read_mails` flag set to True.

        :param path: the relative path from the current position
        to the desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 == unlimited;
        :type how_many: int
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`word.Word` objects
        :param general_stats: the overall stats of the features;
        :type general_stats: associative array {str, :class:`gen_stat.Stat`}
        :param config: contains some general parameters and configurations;
        :type config: :class:`config.Config` object
        :return: a list containing all the mails in the given files.

        """
        return Utils._read_files(path, how_many, True,
                words, general_stats, config)

    @staticmethod
    def read_text(path, how_many, config):
        """
        Read the desidered number of text files from the given path.

        Calls method Utils._read_files, passing the same parameters received,
        with `read_mails` flag set to False.

        :param path: the relative path from the current position
        to the desidered directory;
        :type path: str
        :param how_many: how many files to read. 0 = unlimited;
        :type how_many: int
        :param config: contains some general parameters and configurations;
        :type config: :class:`config.Config` object;
        :return: a list containing all the text in the given files.

        """
        return Utils._read_files(path, how_many, False, [], [], config)

    @staticmethod
    def chunks(l, n):
        """ Yield successive n-sized chunks from l.

        From http://stackoverflow.com/questions/312443 (thanks).

        :param l: the list to be splitted;
        :param n: the size of the generated chunks.

        """

        for i in xrange(0, len(l), n):
            yield l[i: i + n]

    @staticmethod
    def create_stats():
        """
        Defines a new associative array of (str, Stat), containing all the
        overall stats to be evaluated by the Bayes network.

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
        gs['NUMBER']     = Stat("# of numers", 0, 0)
        return gs
