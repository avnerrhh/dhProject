import matplotlib.pyplot as plt
from numpy.random import rand

# Fixing random state for reproducibility

def show_data_in_scatter_graph(geners_dic):
    fig, ax = plt.subplots()
    colores =['red', 'blue', 'green', 'yellow', 'orange', 'black', 'pink','gray']
    i=0
    for key in geners_dic:
        x = []
        y = []
        area = []
        all_colores = []
        for point in geners_dic[key]:
            x.append(point[0])
            y.append(point[1])
            area.append(abs(point[0]-point[1])*314)
            all_colores.append(colores[i])
        i+=1
        ax.scatter(x, y, c=all_colores, s=area, label=key,
                   alpha=0.3, edgecolors='none')


    ax.legend()
    ax.grid(True)
    plt.xlabel('Song Score', fontsize=18)
    plt.ylabel('Comments Score', fontsize=16)
    plt.show()


