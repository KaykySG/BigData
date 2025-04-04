# Primeira parte
import pandas as pd
import pymongo
import urllib.parse

# Definir o caminho do arquivo CSV
csv_path = r"K:\ProjetosGit\BigData\Prova BigData\archive\steam_bkp.csv"

# Ler o CSV usando Pandas
df = pd.read_csv(csv_path)

# Exibir as 5 primeiras linhas
print(df.head())

# Definir usuário e senha
username = "pedrohjs11"
password = "RWsSQOfkMVp4MRbh"

# Codificar a senha (caso tenha caracteres especiais)
password_encoded = urllib.parse.quote_plus(password)

# Criar a URI corretamente formatada
MONGO_URI = f"mongodb+srv://{username}:{password_encoded}@clusterprovafinal.uzmotrb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProvaFinal"

# Conectar ao MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)

# Acessar o banco e a coleção
db = client["steam"]
collection = db["games"]

print("Conexão com MongoDB Atlas estabelecida!")

# Terceira parte
#  Converter DataFrame Pandas para JSON (MongoDB aceita esse formato)
dados_json = df.to_dict(orient="records")

# Inserir os dados na coleção do MongoDB
collection.insert_many(dados_json)

print(" Dados enviados para o MongoDB Atlas com sucesso!")