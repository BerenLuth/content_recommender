from collections import defaultdict
import gnuplot as plot
import io
import gensim
import item_reader as ir

rank_list_filename = "rank_list_{}.dat"
SELECTED_ARTICLE = 100

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

        '''
        #TODO ripristinare il lemmatize
        title = title.split()
        content = content.split()
        text = title + content
        print "## RICORDATI DI TOGLIERE IL COMMENTO AL LEMMATIZE ##"
        '''

        text = gensim.utils.lemmatize(title+ " " +content)

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


def content_recommender(texts, clean_texts):
    print "\n### analyzer.py ###\tcontent_recommender\n"

    lexicon = gensim.corpora.Dictionary(clean_texts)
    #print "\t",lexicon

    corpus = [lexicon.doc2bow(text) for text in clean_texts]

    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    index = gensim.similarities.MatrixSimilarity(corpus_tfidf, num_features=len(lexicon))

    s = raw_input('\tVuoi vedere gli articoli presenti? (y/n) ')
    if s == 'y':
        show_choices(texts)

    selected = eval(raw_input('\n\tScegli da quale articolo vuoi partire (0-999) '))

    scores = index[corpus_tfidf[selected]]

    top = sorted(enumerate(scores), key=lambda (k, v): v, reverse=True)



    #print "\t",top[:10]
    print "\n\n\tArticolo di partenza\n"

    print "\t",texts[selected][1]

    print "\n\n\tArticoli suggeriti\n"
    c=1
    for a,b in top[0:10]:
        b = ("%.2f" % round(b*100,2))
        print "\t",c,"\tsimilarita\':",b,"%\t> ",texts[a][1]
        c +=1
