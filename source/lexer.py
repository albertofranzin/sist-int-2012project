import ply.lex as lex

from gen_stat import Word
from test_stat import Test_word


class Lexer:
    """
    Lexical Analyzer. Use Ply's lexer to identify the tokens and to classify them.
    See http://www.dabeaz.com/ply/ to know how it works.

    """

    def _process_tokens(self, results, in_training, is_spam, words,
                general_stats, params):
        """Process tokens extracted from the training set.

        For every token, extract the value (the word itself)
        and its type (lowercase word, title, link, etc),
        then update all the stats for the word and the mail.
        If the analyzed mail belongs to a training set, then the stats
        are updated according to the (known) class of the mail. Otherwise,
        the stats cannot be associated to any class, since this is yet to
        be detected.

        :param results: the list of tokens recognized;
        :type results: array of tokens
        :param in_training: flag to tell if the lexing is performed during training\
            (`True`) or during validation or testing (`False`). If we are performing\
            the training step, then we know if the mail processed is ham or spam, and
            so we can fill appropriately the `general_stats` array of
            :class:`gen_stat.Stat`, otherwise the array will be filled with
            :class:`test_stat.Test_stat` objects;
        :param is_spam: flag to identify the mail as spam or ham (useless if \
            `in_training == False`);
        :type is_spam: bool
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`gen_stat.Word` objects
        :param general_stats: the overall stats of the features. Feature type may be\
            of two types:\
                :class:`gen_stat.Stat` (`in_training == True`), or\
                :class:`test_stat.Test_stat` (`in_training == False`);
        :param params: contains some general parameters and configurations;
        :type params: associative array

        """

        if in_training:
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
                        # print "Lexer :: process_tokens :: new word :: ", value
                        words[value] = new_word

                # updates general stats, based on the type of the word
                # and the status of the mail (spam/ham). Short words may be
                # of any type (|word| <= threshold), excepting 'WASTE'
                if is_spam:
                    if len(value) <= params['SHORT_THR'] and type != 'WASTE':
                        general_stats['SHORTWORDS'].spam += 1
                    if (len(value) >= params['VERYLONG_THR'] and
                             not (type == 'MAILADDR'
                               or type == 'LINKADDR'
                               or type == 'USERHOST')):
                        general_stats['LOONGWORDS'].spam += 1
                    general_stats[type].spam += 1
                else:
                    if len(value) <= params['SHORT_THR'] and type != 'WASTE':
                        general_stats['SHORTWORDS'].ham += 1
                    if (len(value) >= params['VERYLONG_THR'] and
                             not (type == 'MAILADDR'
                               or type == 'LINKADDR'
                               or type == 'USERHOST')):
                        general_stats['LOONGWORDS'].ham += 1
                    general_stats[type].ham += 1

        else:
            # runs through the list of tokens
            for token in results:

                # extracts type and value from the token
                type, value = token[0], token[1]

                # insert the word into the dictionary (if not read before),
                # or update its stats (if already met)
                # we don't consider words of type 'WASTE' as real words
                if type != 'WASTE':
                    if value in words:
                        words[value].occurrences += 1
                    else:
                        # creates a new Word object for the never-met-before word,
                        # and insert it into the bag
                        new_word = Test_word(1)
                        # print "Lexer :: process_tokens :: new word :: ", value
                        words[value] = new_word

                # updates general stats, based on the type of the word
                # w/o knowing the class of the mail. Short words may be
                # of any type (|word| <= threshold), excepting 'WASTE'
                if len(value) <= params['SHORT_THR'] and type != 'WASTE':
                    general_stats['SHORTWORDS'].count += 1
                if (len(value) >= params['VERYLONG_THR'] and
                         not (type == 'MAILADDR'
                           or type == 'LINKADDR'
                           or type == 'USERHOST')):
                    general_stats['LOONGWORDS'].count += 1
                general_stats[type].count += 1

        # just a check
        # if config.VERBOSE:
        #     print general_stats['LINKADDR'].ham
        #     print general_stats['LINKADDR'].spam

        # looks like that the return is not needed...
        # return (words, general_stats)

    def lexer_words(self, text, in_training, is_spam,
                words, general_stats, params):
        """
        Apply lexical analysis to the text of mails.

        May

        :param text: the text of the mail to be parsed;
        :type text: str
        :param in_training: flag to tell if the lexing is performed during training\
            (`True`) or during validation or testing (`False`). If we are performing\
            the training step, then we know if the mail processed is ham or spam, and
            so we can fill appropriately the `general_stats` array of
            :class:`gen_stat.Stat`, otherwise the array will be filled with
            :class:`test_stat.Test_stat` objects;
        :param is_spam: flag to identify the mail as spam or ham (useless if \
            `in_training == False`);
        :type is_spam: bool
        :param words: the list of words read so far, and their stats;
        :type words: array of :class:`gen_stat.Word` objects
        :param general_stats: the overall stats of the features. Feature type may be\
            of two types:\
                :class:`gen_stat.Stat` (`in_training == True`), or\
                :class:`test_stat.Test_stat` (`in_training == False`);
        :param params: contains some general parameters and configurations;
        :type params: associative array

        """

        # recognize the utf-8 chars
        self.lexer.input(unicode(text))
        # creates empty list for the results
        result = []

        # runs indefinitely until no more tokens are detected
        # gets a new token and inserts it into the list
        while True:
            token = self.lexer.token()
            if not token:
                break
            # print token.value
            result = result + [(token.type, token.value)]
        # if config.VERBOSE:
        #     print result
        self._process_tokens(result, in_training, is_spam,
                words, general_stats, params)

    def __init__(self):
        """
        Constructor: creates the `Ply` lexer and defines all the rules to identify
        and classify the tokens.

        All the ``t_TOKEN()`` methods are defined as inner methods inside here.

        """

        print "Lexer :: tryin' to create ply's lex.lex()"

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
            r'[0-9]+(?:\.[0-9]*)'
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

        self.lexer = lex.lex()
        print "Lexer :: ply's lex.lex() created"
