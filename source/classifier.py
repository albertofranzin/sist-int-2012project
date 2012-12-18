import math


class Classifier:
    """Classify the test set.

    Apply Bayesian logic to classify the mails as spam or ham.

    """

    @staticmethod
    def classify(ws, gs, ovrl_ws, ovrl_gs, config):
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
        :param config: contains some general parameters and configurations;
        :type config: :class:`config.Config` object
        :return: `True` if the mail is classified as spam, `False` if it is\
            considered ham.

        """

        ovrl_words = ovrl_ws.keys()
        smth = config.SMOOTH_VALUE
        ovrl_pspam = 1.0
        ovrl_pham = 1.0
        for word in ws.keys():
            word_count = ws[word].occurrences
            if word in ovrl_words:
                # already met
                s_occ = ovrl_ws[word].spam_occurrences / 1.0 / config.SIZE_OF_BAGS
                h_occ = ovrl_ws[word].ham_occurrences / 1.0 / config.SIZE_OF_BAGS
                t_occ = s_occ + h_occ
                pws = ((s_occ + smth) / (t_occ + 2.0 * smth)) ** word_count
                pwh = ((h_occ + smth) / (t_occ + 2.0 * smth)) ** word_count
                if config.VERBOSE:
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
            ds = math.fabs(ovrl_gs[stat_id].spam / 1.0 / config.SIZE_OF_BAGS - stat)
            dh = math.fabs(ovrl_gs[stat_id].ham / 1.0 / config.SIZE_OF_BAGS - stat)
            prob_gen_spam *= (dh + smth) / (ds + dh + 2.0 * smth)
            prob_gen_ham *= (ds + smth) / (ds + dh + 2.0 * smth)

            if config.VERBOSE:
                if ds < dh:
                    print "-- ", gs[stat_id].description, " is more likely to be spam",
                    if ds + dh > 0:
                        print 1.0 * ds / (1.0 * ds + dh), 1.0 * dh / (1.0 * ds + dh),
                else:
                    print "-- ", gs[stat_id].description, " is more likely to be ham",
                    if ds + dh > 0:
                        print 1.0 * ds / (1.0 * ds + dh), 1.0 * dh / (1.0 * ds + dh),
                print stat, ovrl_gs[stat_id].spam * 1.0 / config.SIZE_OF_BAGS,
                print ovrl_gs[stat_id].ham * 1.0 / config.SIZE_OF_BAGS

        final_prob_spam = 1.0 * prob_gen_spam * config.OVERALL_FEATS_SPAM_W + ovrl_pspam * 1.0 * (1 - config.OVERALL_FEATS_SPAM_W)
        final_prob_ham = 1.0 * prob_gen_ham * config.OVERALL_FEATS_SPAM_W + ovrl_pham * 1.0 * (1 - config.OVERALL_FEATS_SPAM_W)
        if config.VERBOSE:
            print "** **", final_prob_spam, final_prob_ham, "** **"
        #if final_prob_spam > final_prob_ham and
        if (final_prob_spam / (final_prob_spam + final_prob_ham)) >= config.SPAM_THR:
            print "Mail is more likely to be spam",
            ret_val = True
        else:
            print "Mail is more likely to be ham",
            ret_val = False

        print (final_prob_spam / (final_prob_spam + final_prob_ham)) * 100.0

        # raw_input("insert coin to continue...")

        return ret_val
