from fastapi import FastAPI
import pandas as pd
import pymongo
import urllib.parse
from bson.objectid import ObjectId

app = FastAPI()

username = "pedrohjs11"
password = "64IcxNL8vtuMhZ7v"
password_encoded = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://pedrohjs11:{password_encoded}@clusterprova.iptxmnu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProva"
DATABASE = "steam"
COLLECTION = "games"

global_df = None

def carregar_dados():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE]
    collection = db[COLLECTION]
    dados = list(collection.find())
    client.close()
    for documento in dados:
        for chave, valor in documento.items():
            if isinstance(valor, ObjectId):
                documento[chave] = str(valor)
    return pd.DataFrame(dados)

@app.on_event("startup")
async def startup_event():
    global global_df
    global_df = carregar_dados()
    if global_df is not None:
        print("Dados do MongoDB carregados com sucesso na inicialização.")
    else:
        print("Falha ao carregar os dados do MongoDB na inicialização.")

def get_dataframe():
    return global_df

@app.get("/jogos_mais_bem_avaliados")
async def jogos_mais_bem_avaliados():
    df = get_dataframe()
    if df is not None:
        top_jogos = df.nlargest(10, 'positive_ratings').to_dict(orient='records')
        return top_jogos
    return {"error": "Dados não carregados."}

@app.get("/jogos_mais_avaliacoes_ruins")
async def jogos_mais_avaliacoes_ruins():
    df = get_dataframe()
    if df is not None:
        top_jogos = df.nlargest(10, 'negative_ratings').to_dict(orient='records')
        return top_jogos
    return {"error": "Dados não carregados."}

@app.get("/jogos_mais_horas_jogadas")
async def jogos_mais_horas_jogadas():
    df = get_dataframe()
    if df is not None:
        top_jogos = df.nlargest(10, 'average_playtime').to_dict(orient='records')
        return top_jogos
    return {"error": "Dados não carregados."}

@app.get("/generos_mais_recorrentes")
async def generos_mais_recorrentes():
    df = get_dataframe()
    if df is not None:
        generos = df['genres'].str.split(';', expand=True).stack().str.strip().value_counts().nlargest(10).to_dict()
        return generos
    return {"error": "Dados não carregados."}

@app.on_event("startup")
async def startup_event():
    global global_df
    global_df = carregar_dados()
    if global_df is not None:
        global_df['release_date'] = pd.to_datetime(global_df['release_date'], errors='coerce')
        print("Dados do MongoDB carregados com sucesso na inicialização.")
    else:
        print("Falha ao carregar os dados do MongoDB na inicialização.")

def get_dataframe():
    return global_df

@app.get("/games_by_month")
async def games_by_month():
    df = get_dataframe()
    if df is not None:
        # Garante que 'release_date' seja datetime antes de extrair o mês
        if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

        df_not_null = df.dropna(subset=['release_date']).copy() # Remove linhas com datas inválidas

        df_not_null['release_month'] = df_not_null['release_date'].dt.month_name(locale='pt_BR')
        month_counts = df_not_null['release_month'].value_counts().reset_index()
        month_counts.columns = ['month', 'count']
        return month_counts.to_dict(orient='records')
    return {"error": "Dados não carregados."}

@app.get("/publishers_by_year/{year}")
async def publishers_by_year(year: int):
    df = get_dataframe()
    if df is not None:
        df_year = df[df['release_date'].dt.year == year].copy()
        if not df_year.empty:
            publishers_count = df_year['publisher'].str.split(';', expand=True).stack().str.strip().value_counts().nlargest(5).reset_index()
            publishers_count.columns = ['publisher', 'count']
            return publishers_count.to_dict(orient='records')
        return []
    return {"error": "Dados não carregados."}

@app.get("/available_years")
async def available_years():
    df = get_dataframe()
    if df is not None:
        available_years = sorted(df['release_date'].dt.year.dropna().unique().astype(int).tolist())
        return available_years
    return [] # Retorna uma lista vazia em caso de erro ou dados não carregados
