import os

from bs4 import BeautifulSoup

from lexer import Lexer


class Trainer:
    """Trains the network"""

    def __init__(self):
        self.lexer = Lexer()

    def train(self, words, general_stats, config):
        """Read all the given 'ham' mails, or the first SIZE_OF_BAGS if this value is >0.
        Ham mails must be in  /path/to/project/directory/spam/ham/
        Spam mails must be in /path/to/project/directory/spam/spam/
        We are in /path/to/project/directory/
        First, move to the right dir, then one by one read all the mails
        and send them to the lexer.

        """

        # if we don't want to use the entire mail archive for train the system, then
        # we have to keep track of how many mails (of each kind) we have opened
        if config.SIZE_OF_BAGS > 0:
            processed_mails = 0

        os.chdir("spam/ham/")
        # runs through all the files
        for file in os.listdir("."):
            # open the file
            in_file = open(file, "r")
            # read all its content
            mail = in_file.read()
            # close file
            in_file.close()
            print "Processing file", file  # , "\n\n"
            soup = BeautifulSoup(''.join(mail))
            (words, general_stats) = self.lexer.lexer_words(
                    soup.get_text(), False,
                    words, general_stats, config)

            # keep the count of read mails if needed
            if config.SIZE_OF_BAGS > 0:
                processed_mails += 1
                if processed_mails >= config.SIZE_OF_BAGS:
                    processed_mails = 0
                    break

        """Now go for the spam mails. Code works exactly like the above rows.
        We still are in /path/to/project/directory/spam/ham/,
        so we move to the right dir.

        """

        os.chdir("../spam/")
        for file in os.listdir("."):
            in_file = open(file, "r")
            mail = in_file.read()
            in_file.close()
            print "Processing file", file  # , "\n\n"
            soup = BeautifulSoup(''.join(mail))
            (words, general_stats) = self.lexer.lexer_words(
                    soup.get_text(), True,
                    words, general_stats, config)

            if config.SIZE_OF_BAGS > 0:
                processed_mails += 1
                if processed_mails >= config.SIZE_OF_BAGS:
                    break

        return (words, general_stats)

    def trainer_print(self, general_stats):
        for feature in general_stats.itervalues():
            print general_stats[feature].description, "\t\t",
            print general_stats[feature].spam, "\t\t",
            print general_stats[feature].ham
        print feature.description, "\t\t", feature.spam, "\t\t", feature.ham
