import pandas as pd
import plotly.express as px
Grafico_j=pd.read_csv("Tabela_Clubes.csv")
display(Grafico_j.info())
df_2011=Grafico_j[Grafico_j['Ano'] == 2011]
print(df_2011.head())
df=Grafico_j.copy()
#Separar Os times
df["Clubes"] = df["Clubes"].str.split(", ")
#Explodir
df=df.explode("Clubes")
#Media dos Times
media_times = df.groupby("Clubes")["Media_Valor"].mean().sort_values(ascending=False).head(10)
fig=px.bar(
    x=media_times.index,
    y=media_times.values,
    text=media_times.values,
    title="Top 10 Times Com Maior Valor Medio Por Jogador"
)
fig.update_traces(textposition='outside')
fig.show()
