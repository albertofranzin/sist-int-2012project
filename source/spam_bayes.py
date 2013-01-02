"""
.. module::spam_bayes
   :platform: Unix, Windows
   :synopsis: an example of spam classifier using Naive Bayes

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <fabio.palese@gmail.com>

"""

# from config import Config
from naive_bayes import Bayes

if __name__ == '__main__':
    """Main."""

    # create the network
    bayes = Bayes()

    # if we want to use older results, then we can do so,
    # else we can train the network over new data.
    if bayes.params['READ_FROM_FILE']:
        bayes.read_bayes()
    else:
        bayes.train()

    # now check the results, with validation and testing.
    bayes.check()

    # if desidered, then save the results for a future run.
    if bayes.params['WRITE_TO_FILE']:
        bayes.write_bayes()

    # if desidered, classify some unknown mails
    # in other words, now we just USE the classifier...
    if bayes.params['USE_BAYES']:
        bayes.test()
        # still update the configuration - it's Bayes, after all
        if bayes.params['WRITE_TO_FILE']:
            bayes.write_bayes()
