class Classifier:
    """Classify the test set.

    Apply Bayesian logic to classify the mails as spam or ham.

    """

    # def __init__(self):
    #     pass

    # @staticmethod
    # def diffs(a, b, c, d):
    #     pass

    # @staticmethod
    # def classify(mws, mgs, words, general_stats, config):
    #     """
    #     TODO: INSERT DOCUMENTATION HERE!!!
    #     """

    #     print "Classifier :: classify :: begin"
    #     # prob = 1.0
    #     word_list = mws.keys()
    #     ovrl_list = words.keys()
    #     overall_pspam = 1.0
    #     overall_pham = 1.0
    #     print "Classifier :: classify :: loop starts now"
    #     for word in word_list:
    #         if word in ovrl_list:
    #             pspam = words[word].spam_occurrences
    #             pham  = words[word].ham_occurrences
    #             ptot = pspam + pham
    #             # print "word '", word, "' stats : ", pspam, "times spam,", pham, "times ham, ", ptot, "total",
    #             # print pspam / (ptot * 1.0),
    #             # prob *= (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
    #             # print "  prob  ", (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)

    #             prob_spam = (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
    #             prob_ham = (1.0 * pham + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
    #             if prob_spam > prob_ham:
    #                 print "-- ", word, " is more likely to be spam",
    #                 print prob_spam / (prob_spam + prob_ham)
    #             else:
    #                 print "-- ", word, " is more likely to be ham",
    #                 print prob_ham / (prob_spam + prob_ham)

    #             overall_pspam *= (1.0 * pspam + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)
    #             overall_pham *= (1.0 * pham + config.SMOOTH_VALUE) / (1.0 * ptot + config.SMOOTH_VALUE * 2.0)

    #         else:
    #             # prob *= 1
    #             #print "--  word '", word, "' never met before"
    #             # overall_pspam *= 0.9
    #             pass
    #         # print word, prob

    #     # use the overall features stats
    #     prob_gen_spam = 1.0
    #     prob_gen_ham = 1.0
    #     stats = general_stats.keys()
    #     for stat_id in stats:
    #         stat = mgs[stat_id]
    #         prob_gen_ham *= (1.0 * stat.ham + config.SMOOTH_VALUE) / (1.0 * (stat.spam + stat.ham) + 2.0 * config.SMOOTH_VALUE)
    #         prob_gen_spam *= (1.0 * stat.spam + config.SMOOTH_VALUE) / (1.0 * (stat.spam + stat.ham) + 2.0 * config.SMOOTH_VALUE)

    #     print "Classifier :: classify :: done : ", overall_pspam, overall_pham,
    #     print prob_gen_spam, prob_gen_ham

    #     final_stats = prob_gen_spam / (prob_gen_spam + prob_gen_ham)
    #     final_words = overall_pspam / (overall_pham + overall_pspam)

    #     # if overall_pham >= overall_pspam:
    #     print final_words, final_stats
    #     print final_stats * config.OVERALL_FEATS_SPAM_W + final_words * (1 - config.OVERALL_FEATS_SPAM_W)

    #     overall_pspam = overall_pspam * (1 - config.OVERALL_FEATS_SPAM_W) + prob_gen_spam * config.OVERALL_FEATS_SPAM_W
    #     overall_pham = overall_pham * (1 - config.OVERALL_FEATS_SPAM_W) + prob_gen_ham * config.OVERALL_FEATS_SPAM_W
    #     if overall_pspam / (overall_pham + overall_pspam) > config.SPAM_THR:
    #         print "####################################"
    #         print "#                                  #"
    #         print "#  mail is more likely to be spam  #"
    #         print "#                                  #"
    #         print "####################################"
    #         decision = True
    #     else:
    #         print "###################################"
    #         print "#                                 #"
    #         print "#  mail is more likely to be ham  #"
    #         print "#                                 #"
    #         print "###################################"
    #         decision = False

    #     return decision

    @staticmethod
    def classify(ws, gs, ovrl_ws, ovrl_gs):
        """
        Classification function which guesses the class of a mail. The Bayesian logic\
        is applied here.

        The method iterates through all the words identified in the mail,
        and for each one computes how much likely it is for the word to belong
        to a spam mail or to a ham mail. Then it does the same for each general
        feature of the mail. Finally, the method combines the two results
        and tells which class the mail is more likely to be.

        The method relies on the correct tuning of the parameters contained in
        the :class:`config.Config` class.

        :param ws: the list of words of the mail to be classified, and their stats;
        :type ws: array of :class:`test_stat.Test_word` objects
        :param gs: array containing the features encontered in the mail;
        :type gs: array of :class:`test_stat.Test_stat` objects
        :return: `True` if the mail is classified as spam, `False` if it is\
            considered ham.

        """

        ovrl_words = self.words.keys()
        smth = self.config.SMOOTH_VALUE
        ovrl_pspam = 1.0
        ovrl_pham = 1.0
        for word in ws.keys():
            word_count = ws[word].occurrences
            if word in ovrl_words:
                # already met
                s_occ = ovrl_ws[word].spam_occurrences / 1.0 / self.config.SIZE_OF_BAGS
                h_occ = ovrl_ws[word].ham_occurrences / 1.0 / self.config.SIZE_OF_BAGS
                t_occ = s_occ + h_occ
                pws = ((s_occ + smth) / (t_occ + 2.0 * smth)) ** word_count
                pwh = ((h_occ + smth) / (t_occ + 2.0 * smth)) ** word_count
                if pws > pwh:
                    print "-- ", word, " is more likely to be spam",
                    if pws + pwh > 0:
                        print 1.0 * pws / (1.0 * pws + 1.0 * pwh),
                else:
                    print "-- ", word, " is more likely to be ham",
                    if pws + pwh > 0:
                        print 1.0 * pwh / (1.0 * pws + 1.0 * pwh),
                print word_count, s_occ, h_occ

                ovrl_pspam *= pws
                ovrl_pham *= pwh
            else:
                # never met before
                pass

        # compute the prob for the general stats
        prob_gen_spam = 1.0
        prob_gen_ham = 1.0
        stats = gs.keys()
        for stat_id in stats:
            stat = gs[stat_id].count
            ds = math.fabs(ovrl_gs[stat_id].spam / 1.0 / self.config.SIZE_OF_BAGS - stat)
            dh = math.fabs(ovrl_gs[stat_id].ham / 1.0 / self.config.SIZE_OF_BAGS - stat)
            prob_gen_spam *= (dh + smth) / (ds + dh + 2.0 * smth)
            prob_gen_ham *= (ds + smth) / (ds + dh + 2.0 * smth)

            if self.config.VERBOSE:
                if ds < dh:
                    print "-- ", gs[stat_id].description, " is more likely to be spam",
                    if ds + dh > 0:
                        print 1.0 * ds / (1.0 * ds + dh), 1.0 * dh / (1.0 * ds + dh),
                else:
                    print "-- ", gs[stat_id].description, " is more likely to be ham",
                    if ds + dh > 0:
                        print 1.0 * ds / (1.0 * ds + dh), 1.0 * dh / (1.0 * ds + dh),
                print stat, ovrl_gs[stat_id].spam / 1.0 / self.config.SIZE_OF_BAGS,
                print ovrl_gs[stat_id].ham / 1.0 / self.config.SIZE_OF_BAGS

        final_prob_spam = prob_gen_spam * self.config.OVERALL_FEATS_SPAM_W + ovrl_pspam * (1 - self.config.OVERALL_FEATS_SPAM_W)
        final_prob_ham = prob_gen_ham * self.config.OVERALL_FEATS_SPAM_W + ovrl_pham * (1 - self.config.OVERALL_FEATS_SPAM_W)
        print "** **", final_prob_spam, final_prob_ham, "** **"
        #if final_prob_spam > final_prob_ham and
        if (final_prob_spam / (final_prob_spam + final_prob_ham)) >= self.config.SPAM_THR:
            print "Mail is more likely to be spam",
            ret_val = True
        else:
            print "Mail is more likely to be ham",
            ret_val = False

        print (final_prob_spam / (final_prob_spam + final_prob_ham)) * 100.0

        # raw_input("insert coin to continue...")

        return ret_val