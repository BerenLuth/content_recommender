import urllib2
import io
import time
import os.path
import sha
from bs4 import BeautifulSoup as bs

THEVERGE_URL = "http://www.theverge.com/{}/archives/{}"
CATEGORIES = ["microsoft","apple","google","apps","photography","vr-virtual-reality","tech"]
ARTICLE_NAME = "articoli/theverge_{}.txt"
ITEMS_NUMBER = 900


#prende i 10 url dalla pagina web
def get_links_from_archive_page(url):
	page = urllib2.urlopen(url)
	souped = bs(page, 'html.parser')
	#x = souped.find_all('li')
	links = []
	elements = souped.find('ul', {'class':"p-basic-article-list"}).find_all('li')
	for element in elements:
		links.append(element.a['href'])
	return links

#legge il contenuto dell'articolo
def get_content_from_article_page(url):
	page = urllib2.urlopen(url)
	soup = bs(page, 'html.parser')
	try:
		title = soup.title.get_text()
		name = soup.find('span', {'class':'c-byline__item'}).a.get_text()
		text = "\n".join([x.get_text().strip() for x in soup.find('div', {'class':'c-entry-content'}).find_all('p') if x.get_text().strip()])
	except AttributeError as ae:
		print "errore nella lettura dell'articolo " + url
		return None
	return [url, title, name, text]

def save_articles(linklist):
	c = 1	# solo per indicazioni in output
	last_percentage = -1

	# per ogni link costruisco il nome del file
	# se il file non esiste, scarico l'articolo
	for link in linklist:
		filename = ARTICLE_NAME.format(sha.new(link).hexdigest())
		if not file_exist(filename):
			time.sleep(1)
			content = get_content_from_article_page(link)	#recupero il contenuto dell'articolo
			if content != None:
				f = io.open(filename, 'w')
				# il contenuto e' diviso in: url, titolo, autore e testo
				for x in content:
					try:
						f.write(x)
						f.write(u"\n")
					except TypeError:
						pass
						#print "errore nella stampa di: " + x + " nel file"

		# ogni 10 link controllati, verifico la quantita' di articoli presenti in locale
		# se la quantita' e' inferiore a 1000, stampo la percentuale, altrimenti concludo
		c += 1
		if c%10 == 0:
			tmp = downloaded_articles()
			if tmp < 1000:
				if (tmp/10) > last_percentage:
					print str(tmp/10) + "%"
					last_percentage = tmp/10
			else:
				print "100% \n Download completato"
				return

def downloaded_articles():
	return len(os.listdir(os.getcwd() + "/articoli"))

def file_exist(fname):
	return os.path.isfile(fname)

def start():
	print "\n### theverge_downloader.py ###\n"

	# Verifico se esiste la cartella dove salvare gli articoli scaricati, se non esiste la creo
	if not os.path.isdir("articoli"):
		print("Creo la cartella articoli...")
		os.makedirs("articoli")

	print "Articoli presenti: " + str(downloaded_articles())
	# se non sono presenti almeno 1000 articoli lancio il download
	if downloaded_articles() < ITEMS_NUMBER:
		print "Sono necessari almeno 1000 articoli: avvio il download..."
		linklist = list()
		# per ogni categoria recuper i link dall'archivio
		for category in CATEGORIES:
			print "Recupero i link della categoria " + category + "..."
			c = 1
			# valore ideale: 12 cicli +- 1000 articoli
			while c<13:
				page_number = THEVERGE_URL.format(category, c)
				x = get_links_from_archive_page(page_number)
				#print category, len(x)
				linklist.extend(x)
				c += 1

		print len(linklist)

		# Una volta recuperati tutti i link, posso lanciare la funzione
		# che si occupa di scaricare gli articoli e salvarli
		save_articles(linklist)
	else:
		print "Il numero di articoli e' sufficiente"
