"""
.. module::SpamBayes
   :platform: Unix, Windows
   :synopsis: an example of spam classifier using Naive Bayes

.. moduleauthor:: Alberto Franzin <alberto.franzin@gmail.com>
                  Fabio Palese <maildimu@gmail.com>

"""

# import collections
import locale
import os
# import re
import sys

from bs4 import BeautifulSoup
import ply.lex as lex

from gen_stat import Stat
from word import Word


# DEFINE SOME VARIABLES

# associative array for the words and their occurrences
words = {}
# associative array for general stats of some interesting features of the mails
general_stats = {}
general_stats['ALLCAPSW']   = Stat("# of all-caps words", 0, 0)
general_stats['ALPHANUM']   = Stat("# of alphanumerical words", 0, 0)
general_stats['USERHOST']   = Stat("# of string in user/hosts form", 0, 0)
general_stats['LINKADDR']   = Stat("# of links", 0, 0)
general_stats['MAILADDR']   = Stat("# of mail addresses", 0, 0)
general_stats['LOWERCASEW'] = Stat("# of all lowercase words", 0, 0)
general_stats['TITLEW']     = Stat("# of words with only the first letter capital", 0, 0)
general_stats['SHORTWORDS'] = Stat("# of \"short words\"", 0, 0)
general_stats['LOONGWORDS'] = Stat("# of non-address \"very long words\"", 0, 0)
general_stats['WASTE']      = Stat("# of non-valid words", 0, 0)
general_stats['NUMBER']     = Stat("# of numers", 0, 0)

# some constants:
# length of a token to be defined "a short word"
SHORT_THR = 1
# length of a token to be defined "a very long word"
VERYLONG_THR = 20
# size of training sets
SIZE_OF_BAGS = 50

# DEFINE LEX RULES

# possible types for the words
tokens = ('ALLCAPSW',
          'ALPHANUM',  # also known as 'bimbominkia style'
          'USERHOST',
          'LINKADDR',
          'MAILADDR',
          'NUMBER',
          'LOWERCASEW',
          'TITLEW',
          'WASTE'
)

# # special states the lexer can be in - only html tag
# useless if BeautifulSoup's get_text() method is used
# states = (
#     ('htmltag', 'inclusive'),
# )

# identifying tokens: structure is the same for all:
# - regexp to select the token
# - extract the word from the unicode string, and lowercase it
# to avoid lowercase/uppercase troubles when comparing words
# - assigns the type to the token
# - return the token


# is the token a mail address?
def t_MAILADDR(token):
    r'[a-zA-Z0-9\.]+\@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+'
    token.value = str(token.value.lower())
    token.type  = 'MAILADDR'
    return token


# is the token a link?
def t_LINKADDR(token):
    r'http:\/\/[a-zA-Z0-9]+(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+[\/[a-zA-Z0-9\?\-_\.\=\%\#]+]*'
    token.value = str(token.value.lower())
    token.type  = 'LINKADDR'
    return token


# is the token in the 'username@host' form?
def t_USERHOST(token):
    r'[a-zA-Z0-9]+[a-zA-Z-0-9\.]*\@(?:[a-zA-Z0-9]+\.)+'
    token.value = str(token.value.lower())
    token.type  = 'USERHOST'
    return token

# # recognizes an opened HTML tag - useless now
# def t_htmltag(token):
#     r'\<'
#     token.lexer.begin('htmltag')
#     pass

# # recognizes a closed HTML tag - useless now
# def t_htmltag_end(token):
#     r'\>'
#     token.lexer.begin('INITIAL')
#     pass

# recognizes an error in the parsing sequence... wait, what?
# def t_htmltag_error(token):
#     token.lexer.skip(1)
#     pass


# is the token a number or a word containing numbers?
def t_ALPHANUM(token):
    r'[a-zA-Z0-9]*(?:[0-9]+[a-zA-Z]+|[a-zA-Z]+[0-9]+)[a-zA-Z0-9]+'
    token.value = str(token.value.lower())
    token.type  = 'ALPHANUM'
    return token


# is the token a word with the first letter capital
# and all the remaining letters lowercase?
def t_TITLEW(token):
    r'[A-Z][a-z]+'
    token.value = str(token.value.lower())
    token.type  = 'TITLEW'
    return token


# IS THE TOKEN A SCREAMED WORD????
def t_ALLCAPSW(token):
    r'[A-Z][A-Z0-9]*'
    token.value = str(token.value.lower())
    token.type  = 'ALLCAPSW'
    return token


# is the token a number?
def t_NUMBER(token):
    r'[0-9]+'
    token.type = 'NUMBER'
    return token


# is the token a 'normal', all-lowercased word?
def t_LOWERCASEW(token):
    r'[a-z]+'
    token.value = str(token.value)
    token.type  = 'LOWERCASEW'
    return token


# identifies all the remaining chars - considered waste
def t_WASTE(token):
    # r'[\\\+\;\:\-\.\'\$\%\?\!\"\,\#\(\)\/\|\[\]\&\=\-\*\{\}\^\_\@\~\>\<]+'
    r'.'
    token.value = token.value
    token.type  = 'WASTE'
    return token

# list of chars to be ignored (whitespaces)
t_ignore = ' \t\v\b'


# jumps forward if finds a new line ('\n')
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1


# recognizes an error in the parsing sequence
def t_error(t):
    print "Lexer: unexpected character " + t.value[0]
    t.lexer.skip(1)


def process_tokens(results, is_spam):
    """Process tokens extracted from the training set.

    For every token, extract the value (the word itself)
    and its type (lowercase word, title, link, etc),
    then update all the stats for the word and the mail.

    :param results: the list of tokens recognized
    :type results: array of tokens.
    :param is_spam: a flag to identify if the mail if spam or ham
    :type is_spam: bool.

    """

    # flag for building the Word object
    spam_no = 1 if is_spam else 0

    # runs through the list of tokens
    for token in results:

        # extracts type and value from the token
        type, value = token[0], token[1]

        # insert the word into the dictionary (if not read before),
        # or update its stats (if already met)
        # we don't consider words of type 'WASTE' as real words
        if type != 'WASTE':
            if value in words:
                # update the correct stat for the word (already met)
                if is_spam:
                    words[value].spam_occurrences += 1
                else:
                    words[value].ham_occurrences  += 1
            else:
                # creates a new Word object for the never-met-before word,
                # and insert it into the bag
                new_word = Word(spam_no, 1 - spam_no)
                words[value] = new_word

        # updates general stats, based on the type of the word
        # and the status of the mail (spam/ham). Short words may be
        # of any type (|word| <= threshold), excepting 'WASTE'
        if is_spam:
            if len(value) <= SHORT_THR and type != 'WASTE':
                general_stats['SHORTWORDS'].spam += 1
            if (len(value) >= VERYLONG_THR and
                     not (type == 'MAILADDR'
                       or type == 'LINKADDR'
                       or type == 'USERHOST')):
                general_stats['LOONGWORDS'].spam += 1
            general_stats[type].spam += 1
        else:
            if len(value) <= SHORT_THR and type != 'WASTE':
                general_stats['SHORTWORDS'].ham += 1
            if (len(value) >= VERYLONG_THR and
                     not (type == 'MAILADDR'
                       or type == 'LINKADDR'
                       or type == 'USERHOST')):
                general_stats['LOONGWORDS'].ham += 1
            general_stats[type].ham += 1

    # just a check
    # print general_stats['LINKADDR'].spam
    # print general_stats['LINKADDR'].ham


# CREATE LEXER

lexer = lex.lex()


# APPLY LEX

def lexer_words(text, is_spam):
    """Apply lexical analysis to the text of mails.

    as Take input the mail text and its status (spam/ham)
    and extract the valid tokens.

    :param text: the text of the mail to be parsed
    :type text: str.
    :param is_spam: flag to identify the mail as spam or ham
    :type is_spam: bool.

    """
    # recognize the utf-8 chars
    lexer.input(unicode(text))
    # creates empty list for the results
    result = []

    # runs indefinitely until no more tokens are detected
    # gets a new token and inserts it into the list
    while True:
        token = lexer.token()
        if not token:
            break
        # print token.value
        result = result + [(token.type, token.value)]
    # print result
    return process_tokens(result, is_spam)

# if we don't want to use the entire mail archive for train the system, then
# we have to keep track of how many mails (of each kind) we have opened
if SIZE_OF_BAGS > 0:
    i = 0


"""Read all the given 'ham' mails, or the first SIZE_OF_BAGS if this value is >0.
Ham mails must be in  /path/to/project/directory/spam/ham/
Spam mails must be in /path/to/project/directory/spam/spam/
We are in /path/to/project/directory/
First, move to the right dir, then one by one read all the mails
and send them to the lexer.

"""
os.chdir("spam/ham/")
# runs through all the files
for file in os.listdir("."):
    # open the file
    in_file = open(file, "r")
    # read all its content
    mail = in_file.read()
    # close file
    in_file.close()

    print "Processing file", file  # , "\n\n"

    # use BeautifulSoup for extracting useful text, striping out HTML tag chars
    # (using get_text()), and send the mail content to the lexer
    soup = BeautifulSoup(''.join(mail))
    # print soup.prettify()
    # print soup.get_text()
    # for i in soup.contents:
    #   print i
    #soup.encode('utf-8')
    # print lexer_words(soup.get_text())
    lexer_words(soup.get_text(), False)

    # keep the count of read mails if needed
    if SIZE_OF_BAGS > 0:
        i += 1
        if i >= SIZE_OF_BAGS:
            i = 0
            break

"""Now go for the spam mails. Code works exactly like the above rows.
We still are in /path/to/project/directory/spam/ham/,
so we move to the right dir.

"""
os.chdir("../spam/")
for file in os.listdir("."):
    in_file = open(file, "r")
    mail = in_file.read()
    in_file.close()
    print "Processing file", file  # , "\n\n"
    soup = BeautifulSoup(''.join(mail))
    lexer_words(soup.get_text(), True)

    if SIZE_OF_BAGS > 0:
        i += 1
        if i >= SIZE_OF_BAGS:
            i = 0
            break


# for feature in general_stats.itervalues():
#     # print general_stats[feature].description, "\t\t",
#             general_stats[feature].spam, "\t\t",
#             general_stats[feature].ham
#     print feature.description, "\t\t", feature.spam, "\t\t", feature.ham


# code for pretty-printing the results
# slightly adapted from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/, many thanks

locale.setlocale(locale.LC_NUMERIC, "")


def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""
    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)


def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    return max([len(format_num(row[index])) for row in table])


def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """

    col_paddings = []
    firstrow = True
    ll = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 2),
        if firstrow:
            ll.append(len(row[0].ljust(col_paddings[0] + 1)) + 1)
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
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


out = sys.stdout

table = [['word', 'spam', 'ham']]
for item in words.iterkeys():
    table.append([item, words[item].spam_occurrences,
                        words[item].ham_occurrences])

pprint_table(out, table)


table = [['Feature description',
          '# occurrences in spam mails',
          '# occurrences in ham mails']]

for item in general_stats.itervalues():
    table.append([item.description, item.spam, item.ham])

print "\nResults:"


pprint_table(out, table)

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
