from classifier import Classifier
from config import Config
from lexer import Lexer
from utils import Utils


class Tester:
    """
    Performs the testing over a set of unknown-status mails,
    using the trained Bayesian network

    """

    def __init__(self):
        self.config = Config()
        self.lexer = Lexer()

    def test(self, mail, network):
        words = {}
        stats = Utils.create_test_stats()
        self.lexer.lexer_words(mail, False, True, words, stats, self.config)
        result = Classifier.classify(words, stats,
                    network.words, network.general_stats)
        print result
