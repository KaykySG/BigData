from fastapi import FastAPI
import pandas as pd
import pymongo
import urllib.parse
from bson.objectid import ObjectId

app = FastAPI()

# Configurações de conexão com o MongoDB
username = "pedrohjs11"
password = "64IcxNL8vtuMhZ7v"
password_encoded = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://pedrohjs11:{password_encoded}@clusterprova.iptxmnu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProva"
DATABASE = "steam"
COLLECTION = "games"

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
            if isinstance(valor, ObjectId):
                documento[chave] = str(valor)
    return pd.DataFrame(dados)

@app.get("/jogos_mais_bem_avaliados")
async def jogos_mais_bem_avaliados():
    df = carregar_dados()
    top_jogos = df.nlargest(10, 'positive_ratings').to_dict(orient='records')
    return top_jogos

@app.get("/jogos_mais_avaliacoes_ruins")
async def jogos_mais_avaliacoes_ruins():
    df = carregar_dados()
    top_jogos = df.nlargest(10, 'negative_ratings').to_dict(orient='records')
    return top_jogos

@app.get("/jogos_mais_horas_jogadas")
async def jogos_mais_horas_jogadas():
    df = carregar_dados()
    top_jogos = df.nlargest(10, 'average_playtime').to_dict(orient='records')
    return top_jogos

@app.get("/generos_mais_recorrentes")
async def generos_mais_recorrentes():
    df = carregar_dados()
    generos = df['genres'].str.split(';', expand=True).stack().str.strip().value_counts().nlargest(10).to_dict()
    return generos