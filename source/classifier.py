from __future__ import division
import math


class Classifier:
    """Classify an item.

    This class contains the :func:`classifier.Classifier.classify` used to
    assign a class (spam/ham) to a mail, using the statistics computed
    for the processed mail, and the statistics of the training set.

    """

    @staticmethod
    def classify(ws, gs, ovrl_ws, ovrl_gs, params):
        """
        Classification function which guesses the class of a mail. Much of the
        Bayesian theory is applied here.

        The method iterates through all the words identified in the mail,
        and for each one computes how much likely it is for the word to belong
        to a spam mail or to a ham mail. Then it does the same for each general
        feature of the mail. Finally, the method combines the two results
        and tells which class the mail is more likely to be.

        The statistics computed for each mail will be used to update the
        general properties tables, based on the the class computed here.

        The method relies on the correct tuning of the parameters contained in
        the :class:`config.Config` class or set by the user.

        :param ws: the list of words of the mail to be classified, and their stats;
        :type ws: array of :class:`test_stat.Test_word` objects
        :param gs: array containing the features encontered in the mail;
        :type gs: array of :class:`test_stat.Test_stat` objects
        :param ovrl_ws: the list of words and their stats;
        :type ovrl_ws: array of array of :class:`gen_stat.Word`
        :param ovrl_gs: the list of the general statistics for the mail corpus;
        :type ovrl_gs: array of array of :class:`gen_stat.Stat`
        :param params: contains some general parameters and configurations;
        :type params: associative array
        :return: `True` if the mail is classified as spam, `False` if it is\
            considered ham.

        """

        # initialize
        ovrl_words = ovrl_ws.keys()
        smth = params['SMOOTH_VALUE']
        size_of_sets = params['SIZE_OF_BAGS']
        ovrl_pspam = 1.0
        ovrl_pham = 1.0

        # for each work in the mail, compute the probability it brings to the
        # status of the mail.
        for word in ws.keys():
            word_count = ws[word].occurrences

            # if the word was alreasy present in the training set, then calculate
            # its contribute to the probability.
            # See the report to know the theory behind.
            if word in ovrl_words:
                # already met
                # need to convert integers into floating point...

                # compute probabilities |occurrences|/|total mails|
                s_occ = ovrl_ws[word].spam_occurrences / size_of_sets
                h_occ = ovrl_ws[word].ham_occurrences / size_of_sets
                t_occ = s_occ + h_occ

                # if the probability if significant (differs from 0.5 more than the threshold)
                # then use the probability, else discard it
                # (brings very little to the total count)
                if ((math.fabs(s_occ / (s_occ + h_occ) - 0.5) > params['RELEVANCE_THR'])
                            and (s_occ > 2 or h_occ > 2)):
                    pws = ((s_occ + smth) / (t_occ + 2.0 * smth)) ** word_count
                    pwh = ((h_occ + smth) / (t_occ + 2.0 * smth)) ** word_count

                    # print the infos
                    if params['VERBOSE']:
                        if pws > pwh:
                            print "-- ", word, " is more likely to be spam",
                            if pws + pwh > 0:
                                print pws / (pws + pwh),
                        else:
                            print "-- ", word, " is more likely to be ham",
                            if pws + pwh > 0:
                                print pwh / (pws + pwh),
                        print word_count, s_occ, h_occ

                    # update total probs
                    ovrl_pspam *= pws
                    ovrl_pham *= pwh
            else:
                # never met before
                # 'do nothing' seem to be the best action
                pass

        # compute the prob for the general stats
        prob_gen_spam = 1.0
        prob_gen_ham = 1.0
        # iterate through the statistics, compute the contribution to probability
        # in the same way of before
        stats = gs.keys()
        # for stat_id in ['ALLCAPSW', 'LINKADDR', 'MAILADDR', 'SHORTWORDS', 'LOONGWORDS']:  # stats:
        for stat_id in stats:
            # compute deviation from relevance threshold
            stat = gs[stat_id].count
            ds = math.fabs(ovrl_gs[stat_id].spam / size_of_sets - stat)
            dh = math.fabs(ovrl_gs[stat_id].ham / size_of_sets - stat)

            # if contribution is relevant, then update the relative stat
            # (otherwise, again, it brings little contribution to probability)
            if ds + dh > 0:
                if math.fabs(ds / (ds + dh) - 0.5) > params['RELEVANCE_THR']:
                    prob_gen_spam *= (dh + smth) / (ds + dh + 2.0 * smth)
                    prob_gen_ham *= (ds + smth) / (ds + dh + 2.0 * smth)

                    if params['VERBOSE']:
                        if ds < dh:
                            print "-- ", gs[stat_id].description, " is more likely to be spam",
                            if ds + dh > 0:
                                print ds / (ds + dh), dh / (ds + dh),
                        else:
                            print "-- ", gs[stat_id].description, " is more likely to be ham",
                            if ds + dh > 0:
                                print ds / (ds + dh), dh / (ds + dh),
                        print stat, ovrl_gs[stat_id].spam / size_of_sets,
                        print ovrl_gs[stat_id].ham / size_of_sets

        # combine the two probabilities (words and general stats) for both ham & spam
        final_prob_spam = 1.0 * prob_gen_spam * params['OVERALL_FEATS_SPAM_W'] + ovrl_pspam * 1.0 * (1 - params['OVERALL_FEATS_SPAM_W'])
        final_prob_ham = 1.0 * prob_gen_ham * params['OVERALL_FEATS_SPAM_W'] + ovrl_pham * 1.0 * (1 - params['OVERALL_FEATS_SPAM_W'])
        if params['VERBOSE']:
            print "** **", final_prob_spam, final_prob_ham, "** **"

        if (final_prob_spam / (final_prob_spam + final_prob_ham)) >= params['SPAM_THR']:
        # if final_prob_spam >= final_prob_ham:
            print "Mail is more likely to be spam",
            ret_val = True
        else:
            print "Mail is more likely to be ham",
            ret_val = False

        print (final_prob_spam / (final_prob_spam + final_prob_ham)) * 100.0,

        # raw_input("insert coin to continue...")

        return ret_val
