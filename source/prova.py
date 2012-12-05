#!/usr/bin/python

import ply.lex as lex
import re
import os
import string

from bs4 import BeautifulSoup

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

# DEFINE SOME USEFUL THINGS
id_tab = "".join(map(chr, xrange(256)))
tostrip = "".join( c for c in id_tab if not ( c.isalnum() or c.isspace() ) )
# isalnum() == isaplha() or isdigit()

# DEFINE HTML PARSING
class MyHTMLParser(HTMLParser):

  def handle_starttag(self, tag, attrs):
    print "Start tag:", tag
    for attr in attrs:
      print "     attr:", attr

  def handle_endtag(self, tag):
    print "End tag  :", tag

  def handle_data(self, data):
    print "Data     :", data

  def handle_comment(self, data):
    print "Comment  :", data

  def handle_entityref(self, name):
    c = unichr(name2codepoint[name])
    #c = unichr(name)
    print "Named ent:", c

  def handle_charref(self, name):
    if name.startswith('x'):
      c = unichr(int(name[1:], 16))
    else:
      c = unichr(int(name))
    print "Num ent  :", c

  def handle_decl(self, data):
    print "Decl     :", data

parser = MyHTMLParser()

parser.feed('<html><head><title>Ciao</title></head><body>AAAAAJHGJHGJ<a href="http://ciao.com">akshdjkshad</a></body></html>')

# DEFINE LEX RULES

tokens = ( 'ALLCAPSW',
           'ALPHANUM', # also known as 'bimbominkia style'
           'LINKADDR',
           'HTMLTAG',
           'MAILADDR',
           'LOWERCASEW',
           'TITLEW'
         )

def t_MAILADDR(token):
  r'[a-zA-Z0-9]+\@(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+'
  token.value = token.value.lower()
  token.type = 'MAILADDR'
  return token

def t_LINK(token):
  r'http:\/\/[a-zA-Z0-9]+(?:[a-zA-Z0-9]+\.)+[a-zA-Z]+[\/[a-zA-Z0-9\?\-_\.\=\%\#]+]*'
  token.value = token.value.lower()
  token.type = 'LINKADDR'
  return token

def t_HTMLTAG(token):
  r'\<'
  token.value = token.value.lower()
  token.type = 'HTMLTAG'
  return token

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

# PROCESS TOKENS

def process_tokens(result):
  for token in result:
    (type, value) = (token.type, token.value)

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

#mail = """This is a s.p.a.m. m41l, ju
#st F0r EXAMPLE"""

#in_file = open("spam.txt", "r")
#mail = in_file.read()
#in_file.close()

#print valid_words(mail)

#print lexer_words(mail.translate(id_tab, tostrip))


os.chdir("spam/hard_ham/")
for files in os.listdir("."):
  in_file = open(files, "r")
  mail = in_file.read()
  in_file.close()
  print "\n\n\n#############  ", files, "     ########\n\n\n"
  #soup = BeautifulSoup(mail, convertEntities=BeautifulSoup.HTML_ENTITIES)
  parser.feed(mail)
  #print lexer_words(mail)#(mail.translate(id_tab, tostrip))


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
