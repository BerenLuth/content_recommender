from os import listdir
from os.path import isfile, join
import io

ARTICLE_FOLDER = "articoli/{}"

# Prende in input una cartella e restituisce una lista contentente i nomi dei files
def listfiles(files_path):

    onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
    #for file in onlyfiles:
    #    print file
    print "Files letti: " + str(len(onlyfiles))
    return onlyfiles

def file_reader(filename):
    f = io.open(ARTICLE_FOLDER.format(filename), 'r')
    link = f.readline()
    title = f.readline().lower().split()
    author = f.readline()
    tmp_content = f.read().splitlines()

    content = []
    for x in tmp_content:
        content.append(x.lower().split())
    return [link, title, author, content]

def read_stopwords():
    f = io.open("stopwords.txt", 'r')
    return f.read().splitlines()

def remove_stopwords(my_dictionary):
    stopwords = read_stopwords()
    for word in stopwords:
        try:
            del my_dictionary[word]
        except KeyError:
            pass

def start():
    texts = []
    files = listfiles(ARTICLE_FOLDER.format(''))

    #result.append(file_reader(files[0]))
    for x in files:
        texts.append(file_reader(x))
    ''' A questo punto texts contiene tutti gli articoli, titoli, e autori '''

    c = 1
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text[1]:
            frequency[token] += 1
        for x in text[3]:
            for token in x:
                frequency[token] += 1
        c += 1

    remove_stopwords(frequency)
    test = [x for x in sorted(frequency.values()) if x>1][::-1][:500]
    print test
    print "parole trovate: " + str(len(frequency))
    print str(read_stopwords)
