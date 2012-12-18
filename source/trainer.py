"""
.. module::trainer
   :platform: Unix, Windows
   :synopsis: trains the network, computing the stats for the main features
                and for the single words.

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""

from bs4 import BeautifulSoup

from lexer import Lexer


class Trainer:
    """Trains the network, computing the stats for the main features
    and for the single words."""

    def __init__(self):
        """Constructor."""
        self.lexer = Lexer()

    def train(self, mails, is_spam, words, general_stats, config):
        """The proper trainer method.

        For all the mails given, extract the single words and classify them,
        calculating the overall stats for some interesting features to be
        evaluated, and for the single words.

        :param mails: the list of mails.
        :type mails: array of str
        :param is_spam: are the given mails spam?
        :type is_spam: bool
        :param words: the array of stats for the single words detected.
        :type words: array of Word objects
        :param general_stats: the overall stats of the set.
        :type general_stats: array of {str, :class:`gen_stat.Stat`}
        :param config: contains some configurations.
        :type config: :class:`config.Config` object

        """

        print "Trainer :: train :: loop begins"
        for mail in mails:
            # print mail
            soup = BeautifulSoup(''.join(mail))
            self.lexer.lexer_words(soup.get_text(), True, is_spam,
                    words, general_stats, config)
        print "Trainer :: train :: done"

    def trainer_print(self, general_stats):
        """
        Print out the overall stats given. For test purposes.

        :param general_stats: the overall stats to be printed.
        :type general_stats: array of {str, :class:`gen_stat.Stat`}

        """

        for feature in general_stats.itervalues():
            # print general_stats[feature].description, "\t\t",
            # print general_stats[feature].spam, "\t\t",
            # print general_stats[feature].ham
            print feature.description, "\t", feature.spam, "\t", feature.ham
