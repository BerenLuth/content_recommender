import theverge_downloader as tvd
import item_reader as ir
import analyzer as an

if __name__ == '__main__':
    print "\n### main.py ###\n"
    tvd.start()
    texts = ir.start()

    # B.1 - stampa dei dati cosi' come sono stati letti
    an.start_base(texts)

    # B.2 - stampa dei dati dopo la rimozione delle stopwords e di lemmatize
    clean_text = an.start_advanced(texts)

    # B.3 - suggerimento articoli + C - riduzione dimensionale
    an.content_recommender(texts, clean_text)

    print "\n"
