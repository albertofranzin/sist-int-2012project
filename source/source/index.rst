.. SpamBayes documentation master file, created by
   sphinx-quickstart on Fri Dec  7 13:51:56 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

SpamBayes's documentation
=========================

.. toctree::
   :maxdepth: 4

Introduction
------------

This document provides the documentation for the software written by Alberto Franzin and Fabio Palese as part of the examination for the course of Intelligent Systems (Sistemi Intelligenti), a.y. 2012/13, University of Padova, taught by prof. S. Badaloni and prof. F. Sambo.

Our project consists in writing a bayesian spam classifier, using the Naive Bayes approach. We have built a Bayes network that can be configurated, trained and used to perform a check on a set of mails to detect if these ones are spam or good mails, called, from now onwards, 'ham'.

The theory and the practice lying below the project is available in the report and in the slides associated with it. Here we provide instead a reference for the modules written by us, and the way to use them, just in case.

The whole code of the project is available at google code (see below).

Download and installation
+++++++++++++++++++++++++

The code can be found at http://code.google.com/p/sist-int-2012project.

We suggest to use the svn repository available. To download the project, open a terminal, go to the chosen directory and type
`svn checkout http://sist-int-2012project.googlecode.com/svn/ sist-int-2012project`.

Python 2.7 is required. We have not performed any test with older versions, as well as newer ones, e.g. Python 3.0, so we cannot guarantee the correct working under these versions.

To successfully launch the program, you need to fullfill the following dependencies:

1. BeautifulSoup (from the bs4 module) (http://www.crummy.com/software/BeautifulSoup/) to extract the useful informations from the mail structure,
2. Ply (http://www.dabeaz.com/ply/) to extract and identify the tokens.

The documentation for these two modules is available on the respective sites.

The user can configure many aspects of the behaviour of the classifier. This can be done by filling in the `spam_bayes.conf` file, either partially or entirely. If a parameter is unset, the default value will be used.

.. warning:: No checks are performed to verify the correctness of the settings. If the environment is inconsistent with respect to the specifications given here, the software may die at any time during the execution.

Usage
+++++

To manage the settings of the program, open the file `spam_bayes.conf` with your favourite editor and set the parameters to the values you like.

To launch the program, from a terminal type
`python /path/of/the/project/spam_bayes.py`.


Main module
-----------

.. automodule:: spam_bayes
    :members:
    :private-members:
    :special-members:

The :mod:`spam_bayes` module launches the classifier, by creating the bayesian network and using it to classify the mails.

The Bayes network definition
----------------------------

In these modules we have defined the actual Bayes network, and all its operations.

The Naive Bayes class
+++++++++++++++++++++

The :mod:`naive_bayes` module provides the :mod:`naive_bayes.Bayes` class, which contains the informations and the methods needed to perform training, validation and testing.

Its main variables are the arrays of stats of the words and the features filled during the training. These arrays, respectively of type {str, :class:`gen_stat.Word`} and {str, :class:`gen_stat.Stat`}. This class provides also the methods to train and validate the network.

.. automodule:: naive_bayes
    :members:
    :private-members:
    :special-members:

The configuration options manager
+++++++++++++++++++++++++++++++++

This is the module providing the basic configurations which allow the user to customize the behaviour of the software.

.. automodule:: config
    :members:
    :private-members:
    :special-members:

The training class
++++++++++++++++++
In this module 

.. automodule:: trainer
    :members:
    :private-members:
    :special-members:

The classifier class
++++++++++++++++++++

.. automodule:: classifier
    :members:
    :private-members:
    :special-members:

Feature statistics modules
------------------------------

When counting the statistics of the mails, we fall into one of the following two cases:

1. we are training the network, so we process the mails knowing their "spamminess" status. In this case we are working with both spam and ham mails in 'parallel', and we need to keep track of how many times a certain feature appears in spam mails, and how many times the same feature appears in ham mails;
2. we are validating the configuration, or discovering the status of a mail (a set of mails), so we can only count the features found. Of course, since a mail belongs only to one and only one (unknown, so far) class, we need only one value for each feature tracked.

To meet this requirement, we provide two different modules. They are very similar, since they have the same purpose, but are used in different situations.

General stats for training sets
+++++++++++++++++++++++++++++++

The `gen_stat` module contains the general stats for the training step. The two classes contained are:

1. :class:`Stat`, containing the number of featured found in both the spam and ham sets, and
2. :class:`Word`, containing the number of times the word has been found in both the spam and ham sets.

Both the classes contain only the constructor, to initialize the variables, which are public and may be modified directly as needed.

.. automodule:: gen_stat
    :members:
    :special-members:

General stats for validation and test sets
++++++++++++++++++++++++++++++++++++++++++

The `test_stat` module contains the general stats for the validation and testing step, when the status of the mail is unknown. The two classes contained are:

1. :class:`Test_stat`, containing the number of featured found in the mail or in the set, and
2. :class:`Test_word`, containing the number of times the word has been found in the mail or in the set.

Since the purpose of these classes is the same of the ones in the :mod:`gen_stat` module, also in these module both the classes contain only the constructor.

.. automodule:: test_stat
    :members:
    :special-members:

Various tools and utilities
---------------------------

The lexical analyzer
++++++++++++++++++++

This is the module containing the lexical analyzer, based on Ply lexer.

.. automodule:: lexer
    :members:
    :private-members:
    :special-members:

Other utilities
+++++++++++++++

All the generic purpose methods used in different locations are placed in the :class:`utils.Utils` class. Namely, these methods are used to:

* read text from the files found in a given location. In particular, these methods can read text in mail format;
* split a list in a given numbers of equally long lists (the last list may be shorter than the previous ones);
* build an empty array containing the overall stats for the training set, thus discriminating the features found in the spam mails from the ones found in ham mails;
* build an empty array containing the overall stats from a generic mail, without knowing its class (its status, ham or spam).

All these methods are static, so have to be invoked using the
`Utils.method()` syntax.

.. automodule:: utils
    :members:
    :private-members:
    :special-members:
