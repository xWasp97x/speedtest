import pickle
from matplotlib import rcParams
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

rcParams.update({'figure.autolayout': True})

results = pickle.load(open('results.pkl', 'rb'))

df = pd.DataFrame(results)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=df['time'], y=df['download'], name='Download'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['time'], y=df['upload'], name='Upload'), secondary_y=False)
fig.add_trace(go.Scatter(x=df['time'], y=df['ping'], name='Ping'), secondary_y=True)

fig.update_layout(title_text="Speedtest Results")
fig.update_xaxes(title_text="Time")
fig.update_yaxes(title_text="Download/Upload (Mbps)", secondary_y=False)
fig.update_yaxes(title_text="Ping (ms)", secondary_y=True)

fig.show()
