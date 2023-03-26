from dash import Dash, html, dcc, dependencies
import plotly.express as px
import pandas as pd
import os
import datetime as dt

app = Dash(__name__)
#make the app darkmode
app.title = "Action Coca Cola (KO) à partir de abcbourse.com"

modif = 0
df = None

def load_data():
    df = pd.read_csv("donnee_historique.csv",sep=";", parse_dates=["Date"], dayfirst=True)
    last_modified = os.path.getmtime("donnee_historique.csv")
    return df

def create_figure():
    fermeture = px.line(df, x="Date", y="Dernier", title='Prix de fermeture au cours du temps')
    ouverture = px.line(df, x="Date", y="Ouverture", title='Prix d\'ouverture au cours du temps')
    volume = px.line(df, x="Date", y="Volume", title='Volume au cours du temps')
    return [fermeture, ouverture, volume]

@app.callback(dependencies.Output('fermeture', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_fermeture(n):
    if modif != os.path.getmtime("donnee_historique.csv"):
        df = load_data()
        fermeture = create_figure()[0]
        return fermeture
    return fermeture

@app.callback(dependencies.Output('ouverture', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_ouverture(n):
    if modif != os.path.getmtime("donnee_historique.csv"):
        df = load_data()
        ouverture= create_figure()[1]
        return ouverture 
    return ouverture 

@app.callback(dependencies.Output('volume', 'figure'),
              [dependencies.Input('interval-component', 'n_intervals')])
def update_volume(n):
    if modif != os.path.getmtime("donnee_historique.csv"):
        df = load_data()
        volume= create_figure()[2]
        return volume 
    return volume
if __name__ == '__main__':
    df = load_data()
    fermeture,ouverture,volume= create_figure()

    app.layout = html.Div(children=[
        html.H1(children='Cours de Coca', style={'textAlign': 'center'}),

        dcc.Graph(
            id='fermeture',
            figure=fermeture
        ),
        dcc.Graph(
            id='ouverture',
            figure=ouverture
        ),
        dcc.Graph(
            id='volume',
            figure=volume
            ),

        dcc.Interval(
            id='interval-component',
            interval=60*1000, # in milliseconds
            n_intervals=0
        )
    ])
    app.run_server(debug=True,port=8050,host='172.31.4.150')
