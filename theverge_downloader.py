import urllib2, io, time, os.path, bs4
from bs4 import BeautifulSoup as bs

THEVERGE_URL = "http://www.theverge.com/{}/archives/{}"
CATEGORIES = ["microsoft","apple","google","apps","photography","vr-virtual-reality","tech"]
ARTICLE_NAME = "articoli/theverge_{}.txt"


#prende i 10 url dalla pagina web
def get_links_from_archive_page(url):

#legge il contenuto dell'articolo
def get_content_from_article_page(url):

# Verifico se esiste la cartella dove salvare gli articoli scaricati, se non esiste la creo
if not os.path.isdir("articoli"):
	print("Creo la cartella articoli...")
	os.makedirs("articoli")

linklist = list()
for category in CATEGORIES:
    c = 1
    while c<20:
        page_number = THEVERGE_URL.format(category, c)
        linklist += get_links_from_archive_page(archive_page)
        c += 1

c = 1
for link in linklist:
    filename = ARTICLE_NAME.format(c)

    if not os.path.isfile(filename):
        content = get_content_from_article_page(link)
        f = io.open(file, 'w')
        f.write(content)
        c += 1

    else:
        print "File " + str(c) + " gia' esistente"
        c += 1
