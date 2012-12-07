"""
.. module::spam_bayes
   :platform: Unix, Windows
   :synopsis: an example of spam classifier using Naive Bayes

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""

from naive_bayes import Bayes
from trainer import Trainer

if __name__ == '__main__':

    print "main :: tryin' to create the Bayes object"
    bayes = Bayes()
    print "main :: Bayes object created"

    print "main :: tryin' to create the Trainer"
    trainer = Trainer()
    print "main :: Trainer created"

    print "main :: tryin' to train bayes"
    (bayes.words, bayes.general_stats) = trainer.train(bayes.words,
                                bayes.general_stats, bayes.config)
    print "main :: bayes trained"

    print "main :: training: done (... magari...)"

    bayes.bayes_print()

    ########################################
    #                                      #
    # ok, now the classification begins... #
    #                                      #
    ########################################

    # os.chdir("../mine/")
    # for file in os.listdir("."):
    #     in_file = open(file, "r")
    #     mail = in_file.read()
    #     in_file.close()
    #     print "Processing file", file  # , "\n\n"
    #     soup = BeautifulSoup(''.join(mail))
    #     lexer_words(soup.get_text(), True)
