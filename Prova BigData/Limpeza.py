import pandas as pd
import pymongo
import urllib.parse
from bson.objectid import ObjectId

# Configurações de conexão com o MongoDB
username = "pedrohjs11"
password = "RWsSQOfkMVp4MRbh"
password_encoded = urllib.parse.quote_plus(password)
MONGO_URI = f"mongodb+srv://{username}:{password_encoded}@clusterprovafinal.uzmotrb.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProvaFinal"
DATABASE_NAME = "steam"
COLLECTION_NAME = "games"
OUTPUT_CSV_PATH = "steam_dados_tratados.csv"
print("Iniciando o processo de ETL...")

# Extrair dados do MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    data = list(collection.find())
    client.close()
    for document in data:
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
    df = pd.DataFrame(data)
    print("Dados extraídos do MongoDB com sucesso.")
except pymongo.errors.ConnectionFailure as e:
    print(f"Erro ao conectar ao MongoDB: {e}")
    df = None
except Exception as e:
    print(f"Ocorreu um erro durante a extração: {e}")
    df = None

# Transformar os dados
print("\nIniciando o processo de ETL...")

if df is not None:
    columns_to_drop = ['_id', 'steam_appid', 'header_image', 'website', 'developers', 'publishers']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
    print("- Colunas irrelevantes removidas.")

    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].mean(), inplace=True)
    print("- Valores ausentes numéricos preenchidos com a média.")

    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna("N/A", inplace=True)
    print("- Valores ausentes de texto preenchidos com 'N/A'.")

    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    duplicated_rows = initial_rows - len(df)
    if duplicated_rows > 0:
        print(f"- {duplicated_rows} linhas duplicadas removidas.")
    else:
        print("- Nenhuma linha duplicada encontrada.")

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.lower().str.strip()
    print("- Colunas de texto padronizadas (lowercase e sem espaços extras).")

    print("\nProcesso de ETL concluído.")

    # Carregar os dados transformados para um arquivo CSV
    try:
        if df is not None:
            df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"\nDados transformados salvos com sucesso em: {OUTPUT_CSV_PATH}")
        else:
            print("Nenhum DataFrame para salvar em CSV.")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar o arquivo CSV: {e}")
else:
    print("Nenhum dado para transformar e salvar.")

print("\nProcesso de ETL finalizado.")