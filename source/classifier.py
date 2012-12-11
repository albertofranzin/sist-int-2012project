class Classifier:
    """Classify the test set.

    Apply Bayesian logic to classify the mails as spam or ham.

    """

    # def __init__(self):
    #     pass

    @staticmethod
    def diffs(a, b, c, d):
        pass

    @staticmethod
    def classify(mws, mgs, words, general_stats, config):
        """
        TODO: INSERT DOCUMENTATION HERE!!!
        """

        print "Classifier :: classify :: begin"
        # prob = 1.0
        word_list = mws.keys()
        ovrl_list = words.keys()
        overall_pspam = 1.0
        overall_pham = 1.0
        print "Classifier :: classify :: loop starts now"
        for word in word_list:
            if word in ovrl_list:
                pspam = words[word].spam_occurrences
                pham  = words[word].ham_occurrences
                ptot = pspam + pham
                # print "word '", word, "' stats : ", pspam, "times spam,", pham, "times ham, ", ptot, "total",
                # print pspam / (ptot * 1.0),
                # prob *= (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
                # print "  prob  ", (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)

                prob_spam = (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
                prob_ham = (1.0 * pham + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
                if prob_spam > prob_ham:
                    print "-- ", word, " is more likely to be spam",
                    print prob_spam / (prob_spam + prob_ham)
                else:
                    print "-- ", word, " is more likely to be ham",
                    print prob_ham / (prob_spam + prob_ham)

                overall_pspam *= (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
                overall_pham *= (1.0 * pham + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)

            else:
                # prob *= 1
                #print "--  word '", word, "' never met before"
                # overall_pspam *= 0.9
                pass
            # print word, prob

        # use the overall features stats
        prob_gen_spam = 1.0
        prob_gen_ham = 1.0
        stats = general_stats.keys()
        for stat_id in stats:
            stat = mgs[stat_id]
            prob_gen_ham *= (1.0 * stat.ham + config.SMOOTH_VALUE) / (1.0 * (stat.spam + stat.ham) + 2.0 * config.SMOOTH_VALUE)
            prob_gen_spam *= (1.0 * stat.spam + config.SMOOTH_VALUE) / (1.0 * (stat.spam + stat.ham) + 2.0 * config.SMOOTH_VALUE)

        print "Classifier :: classify :: done : ", overall_pspam, overall_pham,
        print prob_gen_spam, prob_gen_ham

        final_stats = prob_gen_spam / (prob_gen_spam + prob_gen_ham)
        final_words = overall_pspam / (overall_pham + overall_pspam)

        # if overall_pham >= overall_pspam:
        print final_words, final_stats
        print final_stats * config.OVERALL_FEATS_SPAM_W + final_words * (1 - config.OVERALL_FEATS_SPAM_W)

        overall_pspam = overall_pspam * (1 - config.OVERALL_FEATS_SPAM_W) + prob_gen_spam * config.OVERALL_FEATS_SPAM_W
        overall_pham = overall_pham * (1 - config.OVERALL_FEATS_SPAM_W) + prob_gen_ham * config.OVERALL_FEATS_SPAM_W
        if overall_pspam / (overall_pham + overall_pspam) > config.SPAM_THR:
            print "####################################"
            print "#                                  #"
            print "#  mail is more likely to be spam  #"
            print "#                                  #"
            print "####################################"
            decision = True
        else:
            print "###################################"
            print "#                                 #"
            print "#  mail is more likely to be ham  #"
            print "#                                 #"
            print "###################################"
            decision = False

        return decision
