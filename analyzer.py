from collections import defaultdict
import gnuplot as plot
import io
from gensim import models, similarities, utils, corpora
import item_reader as ir
import logging

rank_list_filename = "rank_list_{}.dat"
SELECTED_ARTICLE = 100
MY_ARTICLES = [5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
N_SELECTED = len(MY_ARTICLES)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# B.1
def start_base(texts):
    print "\n# B.1 ### analyzer.py ###\tBase analyzer\n"
    filename = rank_list_filename.format("dirty")   #nome per il file del grafico

    frequency = defaultdict(int)    #creo un nuovo dizionario delle occorrenze
    #scorro tutti i testi per calcolare le occorrenze delle parole
    for text in texts:
        for token in text[1].split()+text[3].split():   #concateno titolo [1] e testo[3]
            frequency[token] += 1

    dict_ordered = sorted(frequency, key=frequency.get) #creo una lista contenente le parole ordinate per frequenza

    # stampa di prova
    for word in dict_ordered[::-1][:10]:
        print word, frequency[word]

    plot.print_graph_coordinates(dict_ordered, frequency, filename) #salvo il file per il grafico
    plot.windows_gnuplot_command(filename, "dirty data")    #stampo il grafico

# legge il file delle stopwords
def read_stopwords():
    f = io.open("stopwords.txt", 'r', encoding='utf8')
    return f.read().splitlines()

# rimuove le stopwords dal dizionario
def remove_stopwords(my_dictionary):
    stopwords = read_stopwords()
    for word in stopwords:
        try:
            del my_dictionary[word]
        except KeyError:
            pass

# rimuove le occorrenze singole dal dizionario
def remove_single_occurrence(my_dictionary):
    _to_be_deleted = []
    for element in my_dictionary:
        if my_dictionary[element] == 1:
            _to_be_deleted.append(element)

    for element in _to_be_deleted:
        del my_dictionary[element]

# B.2
def start_advanced(texts):
    print "\n# B.2 ### analyzer.py ###\tAdvanced analyzer\n"
    filename = rank_list_filename.format("clean")   #nome del file per gnuplot

    stopwords = read_stopwords()    #lista contenente le stopwords

    frequency = defaultdict(int)    #dizionario delle occorrenze
    for text in texts:  #conto le occorrenze su ogni testo
        for word in text[1].split()+text[3].split():    #concateno il titolo con il corpo dell'articolo
            frequency[word] += 1

    remove_stopwords(frequency) #rimuovo le stopwords
    remove_single_occurrence(frequency) #rimuovo le occorrenze singole

    clean_text = []
    c = 0
    for article in texts:
        title = ""
        content = ""

        # per ogni parola nel titolo e nel corpo dell'articolo, mantengo solo le parole che
        # non sono presenti nelle stopwords e che hanno piu' di un'occorrenza
        for word in article[1].split():
            if word not in stopwords and frequency[word]>1:
                title += word + " "
        for word in article[3].split():
            if word not in stopwords and frequency[word]>1:
                content += word + " "

        text = utils.lemmatize(title+ " " +content) #lemmatizzo i testi

        clean_text.append(text) #creo una nuova lista con
        c += 1
        if c % 100 == 0:
            print "\t",c/10, "%"    #stampo la percentuale di avanzamento
    print ""

    dict_ordered = sorted(frequency, key=frequency.get) #creo una lista con le parole ordinate per occorrenza

    # stampa di prova
    for word in dict_ordered[::-1][:10]:
        print word, frequency[word]

    plot.print_graph_coordinates(dict_ordered, frequency, filename) #salvo il file per gnuplot
    plot.windows_gnuplot_command(filename, "clean data")    #stampo il grafico

    return clean_text   #ritorno la lista "pulita" che mi servira' per pa parte B.3

#Crea un articolo che corrisponde alla media degli articoli dati
def avg_article_from_articles(selected_articles, corpus):
    # creo un dizionario contentente le occorrenze totali delle parole nei testi dati
    avg_dict = defaultdict(int)
    for article in selected_articles:
        for x,y in corpus[article]:
            avg_dict[x] += y

    # costruisco una lista che andra' inserita in corpus
    # contentente la media delle occorrenze delle parole
    avg_article = []
    for x,y in avg_dict.items():
        avg_article.append((x,y/float(N_SELECTED))) #divido il n totale delle occorrenze per il n di articoli
    return avg_article

def similarity_printer(texts, result_list):
    print "\n\tArticoli di partenza\n"
    for x in MY_ARTICLES:
        title = ir.get_original_title(texts[x][0])
        print "\t",title

    print "\n\n\tArticoli suggeriti\n"
    c=1
    result = [(a,b) for (a,b) in result_list if a not in MY_ARTICLES]   #faccio in modo che non vengano stampati gli articoli di partenza
    for a,b in result[0:21]:   #salto il primo elemento perche' ovviamente essendo l'articolo medio calcolato, non sara' presente in texts
        try:
            b = ("%.2f" % round(b*100,2))
            title = ir.get_original_title(texts[a][0])  #recupero il titolo originale (con identazione e punteggiatura)
            print "\t",c,"\tsimilarita\':",b,"%\t> ",title
            c +=1
        except IndexError:  #se prova a stampare l'articolo fittizio, crea un errore in quanto non e' presente in texts
            pass

# Prende in input un il dizionario e il corpus
# Calcola la matrice di similarita' e successivamente ritorna la lista dei risultati
# calcolari sull'ulrimo elemento (quello aggiunto a mano)
def similarity_calculator(dictionary, corpus):
    index = similarities.MatrixSimilarity(corpus, num_features=len(dictionary))
    scores = index[corpus[-1]]
    return sorted(enumerate(scores), key=lambda (k, v): v, reverse=True) #ordino i risultati e li metto in una lista

def topic_finder(k, corpus_tfidf, dictionary, texts):
    print "\n\n### Individuo i topic ###\tk = ", k
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=k) # initialize an LSI transformation
    corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

    #stampa i topic
    '''
    for i in range(0, lsi.num_topics-1):
        print "Topic #", i, ": ", lsi.print_topic(i)
    '''

    top = similarity_calculator(dictionary, corpus_lsi) #lista ordinata in base alla similarita'
    similarity_printer(texts, top)  #stampa la classifica dei piu' simili

def content_recommender(texts, clean_texts):
    print "\n# B.3 ### analyzer.py ###\tcontent_recommender\n"

    lexicon = corpora.Dictionary(clean_texts)   #dizionario delle parole presenti
    corpus = [lexicon.doc2bow(text) for text in clean_texts]    #rappresentazione degli articoli in base a lexicon e alle occorrenze

    avg_article = avg_article_from_articles(MY_ARTICLES, corpus) # calcolo l'articolo che rappresenta la media degli articoli scelti
    corpus.append(avg_article)   # aggiungo l'articolo a corpus

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]    #corpus modificato in base a tfidf

    top = similarity_calculator(lexicon, corpus_tfidf)  #classifica degli articoli piu' simili
    similarity_printer(texts, top) #stampa la classifica

    print "\n# C ### analyzer.py ###\triduzione dimensionale\n"
    topics = [2,10,950] #cambiare qui i valori di k
    for k in topics:
        topic_finder(k, corpus_tfidf, lexicon, texts)
