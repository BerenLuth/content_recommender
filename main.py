import theverge_downloader as tvd
import item_reader as ir
import analyzer as an

if __name__ == '__main__':
    print "\n### main.py ###\n"
    tvd.start()
    texts = ir.start()
    an.start(texts)
