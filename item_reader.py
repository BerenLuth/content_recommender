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

# TODO rimuovere punteggiatura e caratteri particolari
def text_cleaner(article):
    pass

def start():
    print "\n### item_reader.py ###\n"

    texts = []
    files = listfiles(ARTICLE_FOLDER.format(''))

    for x in files:
        texts.append(file_reader(x))
    # A questo punto texts contiene tutti gli articoli, titoli, e autori


    for article in texts:
        text_cleaner(article)   #NON ANCORA IMPLEMENTATA

    return texts
