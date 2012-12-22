"""
.. module::spam_bayes
   :platform: Unix, Windows
   :synopsis: an example of spam classifier using Naive Bayes

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""

# from config import Config
from naive_bayes import Bayes

if __name__ == '__main__':
    """Main."""

    # print "main :: tryin' to create the Bayes object"
    bayes = Bayes()
    # print "main :: Bayes object created"

    # print "main :: tryin' to train bayes"
    # # bayes train
    # print "main :: bayes trained"

    # print "main :: training: done (... magari...)"

    # # bayes.bayes_print(True, True)

    # print "tryin' to classify"
    # print "..."

    # print "main :: test training"
    bayes.train()
    # print "main :: test classifier"
    # bayes.test_bayes()
