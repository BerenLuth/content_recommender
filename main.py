import theverge_downloader as tvd
import item_reader as ir
import analyzer as an
import gnuplot as plot
import io

if __name__ == '__main__':
    print "\n### main.py ###\n"
    tvd.start()
    texts = ir.start()

    # B.1 - stampa dei dati cosi' come sono stati letti
    an.start_dirty(texts)

    # B.2 - stampa dei dati dopo la rimozione delle stopwords e di lemmatize
    clean_text = an.start_clean(texts)

    # B.3 - suggerimento articoli
    an.content_recommender(texts, clean_text)
