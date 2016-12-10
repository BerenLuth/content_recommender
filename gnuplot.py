from os import system, remove
import io

gnuplot_command = "gnuplot -e \"set term dumb; plot \'{}\' title \'{}\'\""

# Lancia il comando per gnuplot in versione base, stampa il grafico a terminale
def windows_gnuplot_command(filename, title):
    system(gnuplot_command.format(filename, title))

#Lancia il comando per gnuplot con interfaccia grafica e specifica come disegnare il grafico
# NON UTILIZZATA
def linux_gnuplot_command():
    x11_command_1 = u"set style line 1 lc rgb \'#0060ad\' lt 1 lw 2 pt 7 ps 1.5   # --- blue;"
    x11_command_2 = u"plot \'rank_list.dat\' title \'500 most frequent words occurrences\' with linespoints ls 1"
    f = io.open('tmp_gnuplot.gp', 'w')
    f.write((x11_command_1 + " " + x11_command_2))
    system('gnuplot tmp_gnuplot.gp')
    #remove('tmp_gnuplot.gp')

# Utile per capire se e' possibile lanciare l'interfaccia grafica
# NON UTILIZZATA
def X_is_running():
    from subprocess import Popen, PIPE
    p = Popen(["xset", "-q"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    return p.returncode == 0

# prende una lista di occorrenze (ordinata) e la stampa in un formato leggibile da gnuplot
def print_graph_coordinates(rank_list, occurrence, filename):
    f = io.open(filename, 'w')
    f.write(u"#\tx\ty\n")
    c = 0
    for element in rank_list[::-1][:500]:
        f.write(u"\t" + str(c) + "\t" + str(occurrence[element]) + "\n")
        c +=1
    print "\tCreato file ", filename
