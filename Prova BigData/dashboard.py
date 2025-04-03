import streamlit as st
import pandas as pd
import pymongo
import plotly.express as px
import urllib.parse
from bson.objectid import ObjectId # Importação correta

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
    # Converter ObjectId para string
    for documento in dados:
        for chave, valor in documento.items():
            if isinstance(valor, ObjectId): # Alterado para ObjectId
                documento[chave] = str(valor)
    return pd.DataFrame(dados)

df = carregar_dados()

# Jogos mais bem avaliados
st.subheader("Jogos mais bem avaliados")
top_jogos_positivos = df.nlargest(10, 'positive_ratings') # Substitua 'positive_ratings' pela coluna correta
fig_positivos = px.bar(top_jogos_positivos, x='name', y='positive_ratings', labels={'positive_ratings': 'Avaliações Positivas', 'name': 'Nome'})
st.plotly_chart(fig_positivos)

# Jogos com mais avaliações ruins
st.subheader("Jogos com mais avaliações ruins")
top_jogos_negativos = df.nlargest(10, 'negative_ratings') # Substitua 'negative_ratings' pela coluna correta
fig_negativos = px.bar(top_jogos_negativos, x='name', y='negative_ratings', labels={'negative_ratings': 'Avaliações Negativas', 'name': 'Nome'})
st.plotly_chart(fig_negativos)

# Jogos com mais horas jogadas
st.subheader("Jogos com mais horas jogadas")
top_jogos_horas = df.nlargest(10, 'average_playtime') # Substitua 'average_playtime' pela coluna correta
fig_horas = px.bar(top_jogos_horas, x='name', y='average_playtime', labels={'average_playtime': 'Tempo Médio de Jogo', 'name': 'Nome'}) 
st.plotly_chart(fig_horas)

# Gêneros mais recorrentes em jogos
st.subheader("Gêneros mais recorrentes em jogos")
generos = df['genres'].str.split(';', expand=True).stack().str.strip().value_counts().nlargest(10)
fig_generos_pizza = px.pie(names=generos.index, values=generos.values)
st.plotly_chart(fig_generos_pizza)