import theverge_downloader as tvd
import item_reader as ir
import analyzer as an
from os import system, remove
import io

gnuplot_command = "gnuplot -e \"set term dumb; plot \'rank_list.dat\' title \'500 most frequent words occurrences\'\""

def windows_gnuplot_command():
    system(gnuplot_command)

def linux_gnuplot_command():
    x11_command_1 = "set style line 1 lc rgb \'#0060ad\' lt 1 lw 2 pt 7 ps 1.5   # --- blue;"
    x11_command_2 = "plot \'rank_list.dat\' title \'500 most frequent words occurrences\' with linespoints ls 1"
    f = io.open('tmp_gnuplot.gp', 'w')
    f.write(x11_command_1 + x11_command_2)
    system('gnuplot tmp.gp')
    remove('tmp_gnuplot.gp')


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

    windows_gnuplot_command()
    linux_gnuplot_command()
