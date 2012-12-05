#!/usr/bin/python

from bs4 import BeautifulSoup
import ply.lex as lex

import collections
import os
import re

# DEFINE GLOBAL VARIABLES

words = set()
words_stats = set()

# DEFINE LEX RULES

tokens = ( 'ALLCAPSW',
           'ALPHANUM', # also known as 'bimbominkia style'
           'USERHOST',
           'LINKADDR',
           'MAILADDR',
           'LOWERCASEW',
           'TITLEW'
         )

states = (
  ('htmltag','inclusive'),
)

def t_MAILADDR(token):
  r'[a-zA-Z0-9\.]+\@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+'
  token.value = str(token.value.lower())
  token.type = 'MAILADDR'
  return token

def t_LINK(token):
  r'http:\/\/[a-zA-Z0-9]+(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+[\/[a-zA-Z0-9\?\-_\.\=\%\#]+]*'
  token.value = str(token.value.lower())
  token.type = 'LINKADDR'
  return token

def t_USERHOST(token):
  r'[a-zA-Z0-9]+[a-zA-Z-0-9\.]*\@(?:[a-zA-Z0-9]+\.)+'
  token.value = str(token.value.lower())
  token.type = 'USERHOST'
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
  token.type = 'ALPHANUM'
  return token

def t_TITLEW(token):
  r'[A-Z][a-z]+'
  token.value = str(token.value.lower())
  token.type = 'TITLEW'
  return token

def t_ALLCAPSW(token):
  r'[A-Z0-9]+'
  token.value = str(token.value.lower())
  token.type = 'ALLCAPSW'
  return token

def t_LOWERCASEW(token):
  r'[a-z]+'
  token.value = str(token.value)
  token.type = 'LOWERCASEW'
  return token

t_ignore = ' \t\v\b'

def t_newline(t):
  r'\n'
  t.lexer.lineno += 1

def t_error(t):
  print "Lexer: unexpected character " + t.value[0]
  t.lexer.skip(1)

#def valid_words(text):
#  s = re.findall(r'[a-zA-Z0-9]+',text)
#  r = []
#  return s

# PROCESS TOKENS

def process_tokens(results):
  for token in result:
    (type, value) = (token.type, token.value)
    # inserisci la parola (value) nell'insieme di parole, o aumentane il contatore se già presente
    if value in words:
      # recupera da words_stats
      # aggiorna
    else:
      # crea un oggetto o quel che sarà con la parola e le statistiche
      # inserisci in words_stats
    # analizza il tipo ed eventualmente informazioni aggiuntive (es: lunghezza della parola, contesto, ...)
    # è spam o non spam? (magari un parametro della funzione...)

# CREATE LEXER

lexer = lex.lex()

# APPLY LEX

def lexer_words(text):
  lexer.input(unicode(text))
  result = [ ]
  while True:
    token = lexer.token()
    if not token: break
    #print token.value
    result = result + [(token.type, token.value)]
  #return process_tokens(result)
  return result


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
  print lexer_words(soup.get_text())
