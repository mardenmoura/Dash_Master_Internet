from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("atendimentos.xlsx")

# criando o gráfico
fig = px.bar(df, x="nomes", y="Quantidade", color="ID chat", barmode="group", labels={'nomes': 'TÉCNICOS DO DIA - SPA',
    'Quantidade':'NÚMERO DE ATENDIMENTOS'
},
color_discrete_sequence=px.colors.qualitative.T10,template='plotly_dark',text='Quantidade')
fig.update_traces(textposition='inside',texttemplate='%{text:.2s}', textfont_size=30)
fig.update_yaxes(showticklabels=False)
fig.update_layout(title={
    'text' : 'GRÁFICO DE ATENDIMENTO DIÁRIO - SUPORTE AVANÇADO 07/06/2023',
    'y': 0.9,
    'x': 0.5
})
fig.show()
opcoes = list(df['ID chat'].unique())
opcoes.append("Todos atendimentos")


app.layout = html.Div(children=[
    
    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de atendimentos no dia.
    '''),

    dcc.Dropdown(opcoes, value='Todos os atendimentos', id='lista_atendimentos'),

    dcc.Graph(
        id='grafico_quantidade_atendimentos',
        figure=fig
    )
])

@app.callback(
    Output('grafico_quantidade_atendimentos', 'figure'),
    Input('lista_atendimentos', 'value')
)
def update_output(value):
    if value == "Todos atendimentos":
        fig = px.bar(df, x="nomes", y="Quantidade", color="ID chat", barmode="group")
    else:
        tabela_filtrada = df.loc[df['ID chat']==value, :]
        fig = px.bar(tabela_filtrada, x="nomes", y="Quantidade", color="ID chat", barmode="group")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)