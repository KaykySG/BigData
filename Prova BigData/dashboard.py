import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Endpoints da API
API_URL = "http://127.0.0.1:8000"

# Jogos mais bem avaliados
st.subheader("Jogos mais bem avaliados")
response = requests.get(f"{API_URL}/jogos_mais_bem_avaliados")
dados = response.json()
df_positivos = pd.DataFrame(dados)
fig_positivos = px.bar(df_positivos, x='name', y='positive_ratings', labels={'positive_ratings': 'Avaliações Positivas', 'name': 'Nome do Jogo'})
st.plotly_chart(fig_positivos)

# Jogos com mais avaliações ruins
st.subheader("Jogos com mais avaliações ruins")
response = requests.get(f"{API_URL}/jogos_mais_avaliacoes_ruins")
dados = response.json()
df_negativos = pd.DataFrame(dados)
fig_negativos = px.bar(df_negativos, x='name', y='negative_ratings', labels={'negative_ratings': 'Avaliações Negativas', 'name': 'Nome do Jogo'})
st.plotly_chart(fig_negativos)

# Jogos com mais horas jogadas
st.subheader("Jogos com mais horas jogadas")
response = requests.get(f"{API_URL}/jogos_mais_horas_jogadas") 
dados = response.json()
df_horas = pd.DataFrame(dados)
fig_horas = px.bar(df_horas, x='name', y='average_playtime', labels={'average_playtime': 'Tempo Médio de Jogo', 'name': 'Nome do Jogo'})
st.plotly_chart(fig_horas)

# Gêneros mais recorrentes em jogos
st.subheader("Gêneros mais recorrentes em jogos")
response = requests.get(f"{API_URL}/generos_mais_recorrentes")
dados = response.json()
generos = pd.Series(dados)
fig_generos_pizza = px.pie(names=generos.index, values=generos.values)
st.plotly_chart(fig_generos_pizza)