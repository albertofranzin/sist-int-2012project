import csv
import config
from gen_stat import Word

prova = Word(spam_count,ham_count)
# print prova.ham_occurrences

with open('prova.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow([prova])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

with open('prova.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print ', '.join(row)
