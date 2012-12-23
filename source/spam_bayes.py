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

    bayes = Bayes()

    if bayes.params['READ_FROM_FILE']:
        bayes.read_bayes()
    else:
        bayes.train()

    bayes.check()

    if bayes.params['WRITE_ON_FILE']:
        bayes.write_bayes()
