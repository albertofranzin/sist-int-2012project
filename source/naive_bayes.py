import locale
import sys

from config import Config

from gen_stat import Stat


class Bayes():
    """Set some configurations"""

    def __init__(self):
        # associative array for the words and their occurrences
        self.words = {}
        # associative array for general stats of some interesting features of the mails
        self.general_stats = {}
        self.general_stats['ALLCAPSW']   = Stat("# of all-caps words", 0, 0)
        self.general_stats['ALPHANUM']   = Stat("# of alphanumerical words", 0, 0)
        self.general_stats['USERHOST']   = Stat("# of string in user/hosts form", 0, 0)
        self.general_stats['LINKADDR']   = Stat("# of links", 0, 0)
        self.general_stats['MAILADDR']   = Stat("# of mail addresses", 0, 0)
        self.general_stats['LOWERCASEW'] = Stat("# of all lowercase words", 0, 0)
        self.general_stats['TITLEW']     = Stat("# of words with only the first letter capital", 0, 0)
        self.general_stats['SHORTWORDS'] = Stat("# of \"short words\"", 0, 0)
        self.general_stats['LOONGWORDS'] = Stat("# of non-address \"very long words\"", 0, 0)
        self.general_stats['WASTE']      = Stat("# of non-valid words", 0, 0)
        self.general_stats['NUMBER']     = Stat("# of numers", 0, 0)
        print "Bayes :: arrays created"

        # lexer
        # print "Bayes :: tryin' to create the Lexer"
        # self.lexer = Lexer()
        # print "Bayes :: Lexer created"

        # config
        self.config = Config()
        print "Bayes :: Config created"

    # code for pretty-printing the results
    # slightly adapted from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/, many thanks

    def bayes_print(self):
        """Prints out a table of data, padded for alignment

        @param out: Output stream (file-like object)
        @param table: The table to print. A list of lists.
        Each row must have the same number of columns.

        """

        def _format_num(num):
            """Format a number according to given places.
            Adds commas, etc. Will truncate floats into ints!"""
            try:
                inum = int(num)
                return locale.format("%.*f", (0, inum), True)

            except (ValueError, TypeError):
                return str(num)

        def _get_max_width(table, index):
            """Get the maximum width of the given column index"""
            return max([len(_format_num(row[index])) for row in table])

        def _pprint_table(out, table):

            col_paddings = []
            firstrow = True
            ll = []

            for i in range(len(table[0])):
                col_paddings.append(_get_max_width(table, i))

            for row in table:
                # left col
                print >> out, row[0].ljust(col_paddings[0] + 2),
                if firstrow:
                    ll.append(len(row[0].ljust(col_paddings[0] + 1)) + 1)
                # rest of the cols
                for i in range(1, len(row)):
                    col = _format_num(row[i]).rjust(col_paddings[i] + 2)
                    if firstrow:
                        ll.append(len(col))
                    print >> out, " | ", col,
                print >> out
                if firstrow:
                    print >> out, '-' * ll[0],
                    for i in range(1, len(ll)):
                        print >> out, ' | ', '-' * ll[i],
                    print >> out
                    firstrow = False

        locale.setlocale(locale.LC_NUMERIC, "")
        out = sys.stdout

        table = [['word', 'spam', 'ham']]
        for item in self.words.iterkeys():
            table.append([item, self.words[item].spam_occurrences,
                                self.words[item].ham_occurrences])

        _pprint_table(out, table)

        print "\nWords:"
        table = [['Feature description',
                  '# occurrences in spam mails',
                  '# occurrences in ham mails']]

        for item in self.general_stats.itervalues():
            table.append([item.description, item.spam, item.ham])

        print "\nResults:"

        _pprint_table(out, table)
