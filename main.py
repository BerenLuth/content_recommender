import theverge_downloader as tvd
import item_reader as ir
import analyzer as an
from os import system

gnuplot_command = "gnuplot -e \"{}plot \'rank_list.dat\' title \'500 most frequent words\'\""
dumb = "set term dumb; "

def X_is_running():
    from subprocess import Popen, PIPE
    p = Popen(["xset", "-q"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    return p.returncode == 0

if __name__ == '__main__':
    print "\n### main.py ###\n"
    tvd.start()
    texts = ir.start()
    an.start(texts)

    system(gnuplot_command.format(dumb))
