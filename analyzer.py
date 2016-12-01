from collections import defaultdict
import io

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

def remove_single_occurrence(my_dictionary):
    _to_be_deleted = []
    for element in my_dictionary:
        if my_dictionary[element] == 1:
            _to_be_deleted.append(element)

    for element in _to_be_deleted:
        del my_dictionary[element]

def dictionary_creator(texts):
    frequency = defaultdict(int)
    for text in texts:
        for token in text[1]:
            frequency[token] += 1
        for x in text[3]:
            for token in x:
                frequency[token] += 1
    return frequency

def print_graph_coordinates(rank_list, occurrence):
    f = io.open("rank_list.dat", 'w')
    f.write(u"#\tx\ty\n")
    c = 0
    for element in rank_list[::-1][:500]:
        f.write(u"\t" + str(c) + "\t" + str(occurrence[element]) + "\n")
        c +=1

def start(texts):
    print "\n### analyzer.py ###"
    frequency = dictionary_creator(texts)
    remove_stopwords(frequency)
    remove_single_occurrence(frequency)

    dict_ordered = sorted(frequency, key=frequency.get)
    for x in dict_ordered[::-1][:500]:
        print x, frequency[x]

    print_graph_coordinates(dict_ordered, frequency)
