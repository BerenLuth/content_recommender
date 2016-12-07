from os import listdir
from os.path import isfile, join
import io
import re
import sha

ARTICLE_FOLDER = "articoli/{}"
ARTICLE_NAME = "theverge_{}.txt"

# Prende in input una cartella e restituisce una lista contentente i nomi dei files
def listfiles(files_path):

    onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f)) and f != '_link_list.txt']
    #for file in onlyfiles:

    print "\tFiles letti: " + str(len(onlyfiles))
    return onlyfiles

def base_file_reader(filename):
    f = io.open(ARTICLE_FOLDER.format(filename), 'r', encoding='utf8')
    link = f.readline()
    title = f.readline()
    author = f.readline()
    content = f.read()

    return [link, title, author, content]

def file_reader(filename):
    f = base_file_reader(filename)
    link = f[0]
    title = text_cleaner(f[1])
    author = text_cleaner(f[2])
    content = text_cleaner(f[3])

    return [link, title, author, content]

def text_cleaner(article):
    x = ""
    for phrase in article.splitlines():
        x += re.sub('[!"#$%&\'()*+,-./:;<=>?@\[\\\\\]^_`{|}~]', ' ', phrase)
    return x.lower()

def get_original_title(link):
    filename = ARTICLE_NAME.format(sha.new(link[:-1]).hexdigest())  #ricostruisco il nome del file dal link(senza lo \n finale)
    article = base_file_reader(filename)
    return article[1][:-1]  #ritorno il titolo senza lo '\n' finale

def get_original_complete(link):
    filename = ARTICLE_NAME.format(sha.new(link[:-1]).hexdigest())
    article = base_file_reader(filename)
    print "\tTitolo: ", article[1]
    print "\tAutore: ", article[2]
    print "\nArticolo: ", article[3]


def start():
    print "\n### item_reader.py ###\n"

    texts = []
    files = listfiles(ARTICLE_FOLDER.format(''))

    for x in files:
        texts.append(file_reader(x))
    # A questo punto texts contiene tutti gli articoli, titoli, e autori

    return texts
