
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models import Span
from bokeh.palettes import  viridis

import numpy as np
import pandas as pd 


def plot_per(fold_list):

    df = pd.read_csv('/home/dhrumil/Desktop/Lab/RNAWebsite_v1/GeneratePlot/data/foldability_prediction.csv', header=0)
    f_list = df[df['foldability'] > 0]['foldability'].tolist()
    print(len(f_list))

    plot = figure(title="Foldability", tools="box_zoom, pan, save,hover,reset,tap,wheel_zoom" , plot_height = 400 , plot_width = 400)

    hist, edges = np.histogram(f_list, density=False, normed = True,  bins=20)

    hist = hist/len(f_list)

    cdf=np.cumsum(hist)

    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:] , legend = "pdf")

    colors = viridis(len(fold_list))


    plot.line(edges[1:], cdf , line_color= "black", line_width= 3 , legend = 'cdf')
    #plot.line(edges_pdf[1:], hist_pdf_norm, line_color="red", line_width=3)

    vline_list = list()
    for  i , j in zip(fold_list,colors):
        vline = Span(location = i, dimension='height', line_color=j, line_width=3)
        vline_list.append(vline)


    plot.legend.location = "top_left"
    plot.renderers.extend(vline_list)

    script, div = components(plot)

    #show(plot)
    return script, div



