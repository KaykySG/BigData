import pandas as pd
import pymongo
import urllib.parse
from bson.objectid import ObjectId
import matplotlib.pyplot as plt

# Configurações de conexão com o MongoDB
username = "pedrohjs11"
password = "64IcxNL8vtuMhZ7v"
password_encoded = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://pedrohjs11:{password_encoded}@clusterprova.iptxmnu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProva"
DATABASE = "steam"
COLLECTION = "games"

# Carregar os dados do MongoDB
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
df = pd.DataFrame(dados)

# Função para obter o gênero principal de um jogo (primeiro gênero da lista)
def get_main_genre(genres_str):
    if isinstance(genres_str, str):
        genres = genres_str.split(';')
        return genres[0].strip() if genres else 'N/A'
    return 'N/A'

df['main_genre'] = df['genres'].apply(get_main_genre)

# 1. Jogos mais bem avaliados
top_jogos_positivos = df.nlargest(10, 'positive_ratings')
plt.figure(figsize=(12, 7))
for i, row in top_jogos_positivos.iterrows():
    plt.bar(row['name'], row['positive_ratings'], label=row['main_genre'])
plt.xlabel('Nome do Jogo')
plt.ylabel('Avaliações Positivas')
plt.title('Top 10 Jogos Mais Bem Avaliados por Gênero')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Gênero', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 2. Jogos com mais avaliações ruins
top_jogos_negativos = df.nlargest(10, 'negative_ratings')
plt.figure(figsize=(12, 7))
for i, row in top_jogos_negativos.iterrows():
    plt.bar(row['name'], row['negative_ratings'], label=row['main_genre'])
plt.xlabel('Nome do Jogo')
plt.ylabel('Avaliações Negativas')
plt.title('Top 10 Jogos com Mais Avaliações Ruins por Gênero')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Gênero', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 3. Jogos com mais horas jogadas
top_jogos_horas = df.nlargest(10, 'average_playtime')
plt.figure(figsize=(12, 7))
for i, row in top_jogos_horas.iterrows():
    plt.bar(row['name'], row['average_playtime'], label=row['main_genre'])
plt.xlabel('Nome do Jogo')
plt.ylabel('Tempo Médio de Jogo (segundos)')
plt.title('Top 10 Jogos com Mais Horas Jogadas por Gênero')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Gênero', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 4. Gêneros mais recorrentes (mantido como um gráfico separado)
generos_counts = df['genres'].str.split(';', expand=True).stack().str.strip().value_counts().nlargest(10)
plt.figure(figsize=(8, 8))
plt.pie(generos_counts, labels=generos_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Top 10 Gêneros Mais Recorrentes')
plt.axis('equal')
plt.tight_layout()
plt.show()