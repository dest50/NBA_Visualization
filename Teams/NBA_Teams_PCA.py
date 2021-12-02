from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import requests
import wget
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

import plotly.express as px

"""get the dataset"""
df = pd.read_excel("Teams.xlsx")
print(df)

""" preprocessing """
ranks = df['Rank']
labels = df['Team']
X = df.drop('Rank',axis=1)
X = X.drop('Team',axis=1)
X = X.drop('M',axis=1)
print(X)

""" normalize datas """
scaler = StandardScaler()
X = scaler.fit_transform(X)

""" apply the pca """
pca = PCA(n_components=2)
X = pd.DataFrame(pca.fit_transform(X))

""" visualize the result """
X['Team']=labels
X['Ranks']=ranks
print(X.shape)
#"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
fig = px.scatter(x=X[0], y=X[1], hover_name=X["Team"],color=X["Ranks"],title="PCA on the statistics of every team",template="plotly_dark")
fig.show()


