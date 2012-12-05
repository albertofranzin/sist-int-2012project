#!/usr/bin/python

from bs4 import BeautifulSoup
import ply.lex as lex

# import collections
import os
# import re

from Stat import Stat
from Word import Word


# DEFINE GLOBAL VARIABLES

words = {}
general_stats = {}

general_stats['ALLCAPSW']   = Stat(0, 0)
general_stats['ALPHANUM']   = Stat(0, 0)
general_stats['USERHOST']   = Stat(0, 0)
general_stats['LINKADDR']   = Stat(0, 0)
general_stats['MAILADDR']   = Stat(0, 0)
general_stats['LOWERCASEW'] = Stat(0, 0)
general_stats['TITLEW']     = Stat(0, 0)
general_stats['SHORTWORDS'] = Stat(0, 0)
general_stats['WASTE']      = Stat(0, 0)


SHORT_THR = 1


# DEFINE LEX RULES

tokens = ('ALLCAPSW',
          'ALPHANUM',  # also known as 'bimbominkia style'
          'USERHOST',
          'LINKADDR',
          'MAILADDR',
          'LOWERCASEW',
          'TITLEW',
          'WASTE'
)


states = (
    ('htmltag', 'inclusive'),
)


def t_MAILADDR(token):
    r'[a-zA-Z0-9\.]+\@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+'
    token.value = str(token.value.lower())
    token.type  = 'MAILADDR'
    return token


def t_LINK(token):
    r'http:\/\/[a-zA-Z0-9]+(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+[\/[a-zA-Z0-9\?\-_\.\=\%\#]+]*'
    token.value = str(token.value.lower())
    token.type  = 'LINKADDR'
    return token


def t_USERHOST(token):
    r'[a-zA-Z0-9]+[a-zA-Z-0-9\.]*\@(?:[a-zA-Z0-9]+\.)+'
    token.value = str(token.value.lower())
    token.type  = 'USERHOST'
    return token


def t_htmltag(token):
    r'\<'
    token.lexer.begin('htmltag')
    pass


def t_htmltag_end(token):
    r'\>'
    token.lexer.begin('INITIAL')
    pass


def t_htmltag_error(token):
    token.lexer.skip(1)


def t_ALPHANUM(token):
    r'[a-zA-Z0-9]*[0-9]+[a-zA-Z0-9]+'
    token.value = str(token.value.lower())
    token.type  = 'ALPHANUM'
    return token


def t_TITLEW(token):
    r'[A-Z][a-z]+'
    token.value = str(token.value.lower())
    token.type  = 'TITLEW'
    return token


def t_ALLCAPSW(token):
    r'[A-Z0-9]+'
    token.value = str(token.value.lower())
    token.type  = 'ALLCAPSW'
    return token


def t_LOWERCASEW(token):
    r'[a-z]+'
    token.value = str(token.value)
    token.type  = 'LOWERCASEW'
    return token


def t_WASTE(token):
    r'[\\\+\;\:\-\.\'\$\%\?\!\"\,\#\(\)\/\|\[\]\&\=\-\*\{\}\^\_\@\~]+'
    token.value = str(token.value)
    token.type  = 'WASTE'
    return token

t_ignore = ' \t\v\b'


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_error(t):
    print "Lexer: unexpected character " + t.value[0]
    t.lexer.skip(1)


# PROCESS TOKENS

def process_tokens(results, is_spam):
    spam_no = 1 if is_spam else 0
    for token in results:
        type, value = token[0], token[1]
        # inserisci la parola (value) nell'insieme di parole, o aumentane il contatore se gia' presente
        if value in words:  # words.has_key(value):
            # recupera da words e aggiorna i valori
            words[value].total_occurrences += 1
            if is_spam:
                words[value].spam_occurrences += 1
        else:
            # crea un oggetto o quel che sara' con la parola e le statistiche
            stats = Word(1, spam_no)
            # inserisci in words_stats
            words[value] = stats
        # analizza il tipo ed eventualmente informazioni aggiuntive (es: lunghezza della parola, contesto, ...)
        if is_spam:
            if len(value) == 1:
                general_stats['SHORTWORDS'].spam += 1
            general_stats[type].spam += 1
        else:
            if len(value) == 1:
                general_stats['SHORTWORDS'].ham += 1
            general_stats[type].ham += 1
    print general_stats['LINKADDR'].spam
    print general_stats['LINKADDR'].ham


# CREATE LEXER

lexer = lex.lex()


# APPLY LEX

def lexer_words(text):
    lexer.input(unicode(text))
    result = []
    while True:
        token = lexer.token()
        if not token:
            break
        #print token.value
        result = result + [(token.type, token.value)]
    return process_tokens(result, False)
    #return result


os.chdir("spam/hard_ham/")
for files in os.listdir("."):
    in_file = open(files, "r")
    mail = in_file.read()
    in_file.close()
    print "\n\n\n\n\n#############################################   ", files, "  ############\n\n\n"
    soup = BeautifulSoup(''.join(mail))
    # print soup.prettify()
    # print soup.get_text()
    # for i in soup.contents:
    #   print i
    #soup.encode('utf-8')
    # print lexer_words(soup.get_text())
    lexer_words(soup.get_text())


print general_stats['LINKADDR'].spam
print general_stats['LINKADDR'].ham
