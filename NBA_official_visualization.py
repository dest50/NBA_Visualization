import time
import pandas as pd
import numpy as np
import pickle
from scipy import stats
import scipy
from itertools import cycle

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline



def palette():
    # Palette
    p1 = ['#000000', '#1d4289', '#f5f6f1', '#c7102e']
    p2 = ['#000000', '#542583', '#fea500', '#6e518c', '#fdc42f', '#8a6bad', '#acacac', '#f4f3eb']
    p3 = ['#000000', '#98012e', '#f7a21e', '#f5f6f1']
    p4 = ['#0a223e', '#2a5134', '#edae56', '#f5f6f1']
    p5 = ['#000000', '#007932', '#ad3535', '#f5f6f1']
    p6 = ['#1e1160', '#e5601f', '#f8a019', '#f5f6f1']
    p7 = ['#071e3e', '#b4b0b2', '#fdbb2f', '#f5f6f1']
    p8 = ['#000000', '#5d6571', '#5b2b81', '#f5f6f1']
    names = ['NBA','Los-Angeles Lakers','Miami Heat','Utah Jazz','Boston Celtics','Phoenix suns','Indiana Pacers','Sacramento Kings']

##    palettes = [p1, p2, p3, p4, p5, p6, p7, p8]
##    for i,palette in enumerate(palettes):
##        sns.palplot(palette)
##        plt.title(names[i]+' palette',loc='left',fontfamily='serif',fontsize=15,y=1.2)

    sns.palplot(p2)
    plt.title('Los-Angeles Lakers palette',loc='left',fontfamily='serif',fontsize=15,y=1.2)
    plt.show()
    return p2
    
    
#################################################################################################################################
#                                                                                                                               #
#                                                     ANALYSE DES POSTES                                                        #
#                                                                                                                               #
#################################################################################################################################
def plot_taille_poids(df):
    fig = px.scatter(df, x='Taille', y='Poids',
                     color='PDV',
                     hover_name="PLAYER",
                     marginal_y = "box",#histogram
                     marginal_x = "box",#histogram
                     title='Gabarit des joueurs en fonction de leur poste')
    return fig

def taille_distribution(df):
    fig = px.histogram(df['Taille'], nbins=50)
    #fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

    mean_human = 178.4
    std_human = 7.59

    x_pdf = np.linspace(140, 240, 200)
    y_pdf = scipy.stats.norm.pdf(x_pdf, mean_human, std_human)

    x_pdf2 = np.linspace(140, 240, 200)
    y_pdf2 = scipy.stats.norm.pdf(x_pdf, (df['Taille']*100).mean(), (df['Taille']*100).std())

    # Plotly
    fig = go.Figure()
##    fig.add_trace(
##        go.Histogram(
##            x=df['Taille']*100,
##            histnorm='probability density',
##            nbinsx=15,
##            name='Taille des joueurs de la NBA',
##        ))
    fig.add_trace(
        go.Scatter(
            x=x_pdf, y=y_pdf,
            line=dict(color="#542583"),
            fill='tozeroy',
            fillcolor='rgba(84, 37, 131, 0.5)',
            name='Distribution de la taille des hommes',
        ))
    fig.add_trace(
        go.Scatter(
            x=x_pdf2,y=y_pdf2,
            line=dict(color="#fea500"),
            fill='tozeroy',
            fillcolor = 'rgba(254, 165, 0, 0.5)',
            name='Distribution de la taille des joueurs de la NBA',
        ))

    # Seaborn
    sns.lineplot(x_pdf, y_pdf, lw=2, label='pdf', color='red')                                                   
    sns.lineplot(x_pdf2, y_pdf2, lw=2, label='pdf2', color='blue')
    sns.histplot(df['Taille']*100, kde=False, stat='density', label='samples', color='lightblue')
    plt.legend()
    #plt.show()

    return fig
    

def plot_type_paniers(df):
    """Nb de paniers 3pts et 2pts en fct du poste"""
    fig = go.Figure()

    postes = list(df['PDV'].unique())
    palette = ['#000000', '#542583', '#fea500', '#6e518c', '#fdc42f', '#8a6bad', '#acacac', '#f4f3eb']
    colors = ['#000000','#542583','#fea500']
    caracs = ['FG%','3P%']#"%FGA\n3PT"
    for i,p in enumerate(postes):
        df_plot = df[df['PDV'] == p]
        fig.add_trace(go.Box(
            y=list(df_plot[caracs[0]])+list(df_plot[caracs[1]]),
            x=[caracs[0] for _ in range(df_plot.shape[0])]+[caracs[1] for _ in range(df_plot.shape[0])],
            name=p,
            marker_color=colors[i]))
    fig.update_layout(
        yaxis_title='normalized moisture',
        boxmode='group'
    )

##    ANALYSE :
##        - Le C est le meilleur buteur à 2pts mais le pire à 3pts
##        - Le G c'est legèrement l'inverse
##        - Le F est équilibré
     
    return fig


#################################################################################################################################
#                                                                                                                               #
#                                                   ANALYSE GLOBALE JOUEUERS NBA                                                #
#                                                                                                                               #
#################################################################################################################################

def map_plot(df):
    df_count = df.groupby(['country','iso_alpha']).size()

    df_viz = pd.DataFrame()
    df_viz['country'] = [i[0] for i in df_count.index]
    df_viz['iso_alpha'] = [i[1] for i in df_count.index]
    df_viz['count'] = list(df_count.apply(lambda x:np.log(x)))
    df_viz['taille'] = list(df.groupby('iso_alpha')['Taille'].mean())

    fig = px.choropleth(df_viz, locations="iso_alpha",
                        color="count",
                        hover_name="country",
                        color_continuous_scale=px.colors.sequential.Plasma)
    return fig


def histogram_tailles(df):
    """Deux courbed de distribution:
        - Taille des joueurs de la nba
        - Taille des hommes (dans la même tranche d'âge)"""
    pass

#################################################################################################################################
#                                                                                                                               #
#                                                           STATISTIQUES                                                        #
#                                                                                                                               #
#################################################################################################################################
def pca_plot(df):
    print(df.dtypes.to_string())
    pca = make_pipeline(StandardScaler(), PCA(n_components=2))
    
    x = df[["FG%","3P%","FT%","+/-","AST%","OREB%","DREB%","REB%","%FGA\n2PT","%FGA\n3PT","%PTS","%REB","%TOV","%STL","%BLK","%PF","3FGM\n%UAST"]]

    x = list(pca.fit_transform(np.array(x)))
    
    fig = px.scatter(x=[i[0] for i in x], y=[i[1] for i in x],
                     color=df.index,
                     hover_name=df["PLAYER"],
                     title='Some awesome visualization')

    #fig.layout.paper_bgcolor = '#FFFFFF'
    #fig.layout.plot_bgcolor = '#FFFFFF'
    return fig



#################################################################################################################################
#                                                                                                                               #
#                                                               MAIN                                                            #
#                                                                                                                               #
#################################################################################################################################

if __name__ == '__main__':

    df = pd.read_csv('datasets/df_players_merged.csv').drop(["Unnamed: 0"], axis=1)

    palette()

    #fig = pca_plot(df)
    #fig = plot_taille_poids(df_players)
    #fig = map_plot(df_players)
    #fig = plot_type_paniers(df)
    fig = taille_distribution(df)
    fig.show()
    




    








    
