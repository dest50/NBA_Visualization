
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px

"""get the dataset"""
df = pd.read_excel("datasets/df_players_merged.xlsx")
print(df)

attempted = df['FGA']
scored = df['FGM']

"""make the linear regression"""
X = attempted.values.reshape(-1,1)
y = scored
regression = LinearRegression()
regression.fit(X,y)

x_range = np.linspace(X.min(), X.max(), 100)
y_range = regression.predict(x_range.reshape(-1, 1))

"""identifying best shooters"""
df['best_worst'] = (scored-attempted*regression.coef_)
df=df.sort_values(by=['best_worst'])

df['best_worst'][:5]=-100 #set the five worst to -1 -> in blue on the graphic
df['best_worst'][-5:]=100 #set the five best to 1 -> in yellow on the graphic
df['best_worst'][5:-5]=0 #set the other to 0

df = df.rename(columns={'FGA': 'Field Goals Attempted Per Match', 'FGM': 'Field Goals Scored Per Match'})
"""plot the graph"""
fig = px.scatter(df,x='Field Goals Attempted Per Match', y='Field Goals Scored Per Match', hover_name='PLAYER',title="2 Points",template="plotly_white",color='best_worst')
fig.add_traces(go.Scatter(x=x_range, y=y_range, name=' '))
fig.show()

