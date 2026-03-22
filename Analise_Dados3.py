import streamlit as st
import pandas as pd
import plotly.express as px
#Titulo e Descricao
st.title("📊 Dashboard do Campeonato Brasileiro de 2008 a 2017")
st.write("Este Dashboard Interativo permite analisar os dados do campeonato Brasileiro de 2008 a 2017")
#Carregar os Dados 
df=pd.read_csv("Tabela_Clubes.csv")
#Proteger os dados/Separar Gols
if not df.empty and df["GolsF/S"].str.contains(":", na=False).any():
    gols = df["GolsF/S"].str.split(":", expand=True)

    df["Gols_Feitos"] = gols[0].astype(int)
    df["Gols_Sofridos"] = gols[1].astype(int)
#Limpar Dados
df=df.dropna(subset=["GolsF/S"])
df = df.drop(columns=["Unnamed: 13", "Unnamed: 14", "Unnamed: 15", "Unnamed: 16"])
#Filtros Interativos
st.sidebar.header("Filtros")
ano = st.sidebar.multiselect("Escolha o Ano:",
    options=df["Ano"].unique(),
    default=df["Ano"].unique()
)
df = df[df["Ano"].isin(ano)]
clubes=st.sidebar.multiselect("Escolha o Clube:",
    options=df["Clubes"].unique(),
    default=df["Clubes"].unique()
)
df=df[df["Clubes"].isin(clubes)]

#Converter Idade
df["Idade_Media"] = df["Idade_Media"].str.replace(",",".").astype(float)
#Validacao
if df.empty:
    st.warning("Nenhum Dado Encontrado Para os Filtros Selecionados")
else:
    st.subheader("Resumo")
    col1,col2,col3 = st.columns(3)
    col1.metric("Total de Clubes", df["Clubes"].nunique())
    col2.metric("Media de Vitorias",int(df["Vitorias"].mean()))
    st.divider()
    col1, col2 = st.columns(2)
    with col1 :
        st.subheader("Posicao vs Valor Medio")
        fig1=px.scatter(df,x="Pos.",y="Media_Valor",color="Clubes",size="Valor_total")
        fig1.update_layout(xaxis=dict(autorange="reversed"))
        st.plotly_chart(fig1,use_container_width=True)
    with col2:
        st.subheader("Media Por Posição")
        media_posicao = df.groupby("Pos.")["Media_Valor"].mean().reset_index()
        fig2 = px.line(media_posicao,x="Pos.",y="Media_Valor",markers=True)
        st.plotly_chart(fig2,use_container_width=True)
