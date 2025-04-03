import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px
import urllib.parse

# Configurações de conexão com o MongoDB
username = "pedrohjs11"
password = "64IcxNL8vtuMhZ7v"
password_encoded = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://pedrohjs11:{password_encoded}@clusterprova.iptxmnu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProva"
DATABASE = "steam"
COLLECTION = "games"

@st.cache_data
def carregar_dados():
    """Carrega os dados do MongoDB e retorna um DataFrame Pandas."""
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE]
    collection = db[COLLECTION]
    dados = list(collection.find())
    client.close()
    return pd.DataFrame(dados)

df = carregar_dados()

# Gráfico de barras interativo
st.subheader("Gráfico de Barras")
coluna_x = st.selectbox("Selecione a coluna para o eixo X:", df.columns)
coluna_y = st.selectbox("Selecione a coluna para o eixo Y:", df.select_dtypes(include=['number']).columns)
fig_barras = px.bar(df, x=coluna_x, y=coluna_y)
st.plotly_chart(fig_barras)

# Gráfico de dispersão interativo
st.subheader("Gráfico de Dispersão")
coluna_x_disp = st.selectbox("Selecione a coluna para o eixo X (dispersão):", df.columns)
coluna_y_disp = st.selectbox("Selecione a coluna para o eixo Y (dispersão):", df.select_dtypes(include=['number']).columns, key="disp_y")
fig_dispersao = px.scatter(df, x=coluna_x_disp, y=coluna_y_disp)
st.plotly_chart(fig_dispersao)

# Tabela interativa
st.subheader("Tabela de Dados")
st.dataframe(df)