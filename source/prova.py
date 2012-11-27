#!/usr/bin/python

import ply.lex as lex
import re
import string

# DEFINE SOME USEFUL THINGS
id_tab = "".join(map(chr, xrange(256)))
tostrip = "".join( c for c in id_tab if not ( c.isalnum() or c.isspace() ) )
# isalnum() == isaplha() or isdigit()

# DEFINE LEX RULES

tokens = ( 'ALLCAPSW',
           'ALPHANUM', # also known as 'bimbominkia style'
           'LOWERCASEW',
           'TITLEW'
         )

def t_ALPHANUM(token):
  r'[a-zA-Z0-9]*[0-9]+[a-zA-Z0-9]+'
  token.value = token.value.lower()
  token.type = 'ALPHANUM'
  return token

def t_TITLEW(token):
  r'[A-Z][a-z]+'
  token.value = token.value.lower()
  token.type = 'TITLEW'
  return token

def t_ALLCAPSW(token):
  r'[A-Z0-9]+'
  token.value = token.value.lower()
  token.type = 'ALLCAPSW'
  return token

def t_LOWERCASEW(token):
  r'[a-z]+'
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

# CREATE LEXER

lexer = lex.lex()

# APPLY LEX

def lexer_words(text):
  lexer.input(text)
  result = [ ]
  while True:
    token = lexer.token()
    if not token: break
    #print token.value
    result = result + [(token.type, token.value)]
  return result

# TEST

mail = """This is a s.p.a.m. m41l, ju
st F0r EXAMPLE"""

#print valid_words(mail)

print lexer_words(mail.translate(id_tab, tostrip))


###############################
##############################
#############################

#s = "hello world! how are you? 0"

# Short version
# print filter(lambda c: c.isalpha(), s)

# Faster version for long ASCII strings:
#id_tab = "".join(map(chr, xrange(256)))
#tostrip = "".join( c for c in id_tab if not ( c.isalpha() or c.isdigit() or c.isspace() ) )
#print s.translate(id_tab, tostrip)

# Using regular expressions
# print re.sub("[^A-Za-z]", "", s)
