from collections import defaultdict
import gnuplot as plot
import io
from gensim import models, similarities, utils, corpora
import item_reader as ir
import logging

rank_list_filename = "rank_list_{}.dat"
SELECTED_ARTICLE = 100
MY_ARTICLES = [20,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950]
N_SELECTED = len(MY_ARTICLES)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def print_graph_coordinates(rank_list, occurrence, filename):
    f = io.open(filename, 'w')
    f.write(u"#\tx\ty\n")
    c = 0
    for element in rank_list[::-1][:500]:
        f.write(u"\t" + str(c) + "\t" + str(occurrence[element]) + "\n")
        c +=1
    print "\tCreato file ", filename

def show_choices(texts):
    c=0
    for article in texts:
        print c,article[1]
        c += 1

def start_base(texts):
    print "\n### analyzer.py ###\tBase analyzer\n"
    filename = rank_list_filename.format("dirty")

    frequency = defaultdict(int)
    for text in texts:
        for token in text[1].split()+text[3].split():
            frequency[token] += 1

    dict_ordered = sorted(frequency, key=frequency.get)

    for word in dict_ordered[::-1][:10]:
        print word, frequency[word]

    print_graph_coordinates(dict_ordered, frequency, filename)
    plot.windows_gnuplot_command(filename, "dirty data")


def read_stopwords():
    f = io.open("stopwords.txt", 'r', encoding='utf8')
    return f.read().splitlines()

def remove_stopwords(my_dictionary):
    stopwords = read_stopwords()
    for word in stopwords:
        try:
            del my_dictionary[word]
        except KeyError:
            pass

def remove_single_occurrence(my_dictionary):
    _to_be_deleted = []
    for element in my_dictionary:
        if my_dictionary[element] == 1:
            _to_be_deleted.append(element)

    for element in _to_be_deleted:
        del my_dictionary[element]


def start_advanced(texts):
    print "\n### analyzer.py ###\tAdvanced analyzer\n"
    filename = rank_list_filename.format("clean")

    stopwords = read_stopwords()

    frequency = defaultdict(int)
    for text in texts:
        for word in text[1].split()+text[2].split():
            frequency[word] += 1

    remove_stopwords(frequency)
    remove_single_occurrence(frequency)

    clean_text = []
    c = 0
    for article in texts:
        title = ""
        content = ""

        for word in article[1].split():
            if word not in stopwords and frequency[word]>1:
                title += word + " "
        for word in article[3].split():
            if word not in stopwords and frequency[word]>1:
                content += word + " "

        text = utils.lemmatize(title+ " " +content)

        clean_text.append(text)
        c += 1
        if c % 100 == 0:
            print "\t",c/10, "%"
    print ""

    dict_ordered = sorted(frequency, key=frequency.get)

    '''
    for x in dict_ordered[::-1][:100]:
        print x, frequency[x]
    '''

    print_graph_coordinates(dict_ordered, frequency, filename)
    plot.windows_gnuplot_command(filename, "clean data")

    return clean_text

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
    for a,b in result[1:21]:   #salto il primo elemento perche' ovviamente essendo l'articolo medio calcolato, non sara' presente in texts
        b = ("%.2f" % round(b*100,2))
        title = ir.get_original_title(texts[a][0])  #recupero il titolo originale (con identazione e punteggiatura)
        print "\t",c,"\tsimilarita\':",b,"%\t> ",title
        c +=1

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

    for i in range(0, lsi.num_topics-1):
        print "Topic #", i, ": ", lsi.print_topic(i)

    top = similarity_calculator(dictionary, corpus_lsi)
    similarity_printer(texts, top)

def content_recommender(texts, clean_texts):
    print "\n### analyzer.py ###\tcontent_recommender\n"

    lexicon = corpora.Dictionary(clean_texts)
    corpus = [lexicon.doc2bow(text) for text in clean_texts]

    avg_article = avg_article_from_articles(MY_ARTICLES, corpus) # calcolo l'articolo che rappresenta la media degli articoli scelti
    corpus.append(avg_article)   # aggiungo l'articolo a corpus

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    top = similarity_calculator(lexicon, corpus_tfidf)
    similarity_printer(texts, top)

    topics = [2,950]
    for k in topics:
        topic_finder(k, corpus_tfidf, lexicon, texts)
