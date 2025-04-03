import pymongo
import urllib.parse

def testar_conexao_mongodb(uri):
    """Tenta se conectar ao MongoDB Atlas e imprime o resultado."""
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=10000)  # Timeout de 10 segundos
        client.server_info()  # Força a conexão e obtém informações do servidor
        print("Conexão com o MongoDB Atlas estabelecida com sucesso!")
        return True
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"Falha na conexão com o MongoDB Atlas: {e}")
        return False
    except pymongo.errors.ConnectionFailure as e:
        print(f"Falha na conexão com o MongoDB Atlas: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

# Substitua pelas suas credenciais e URI
username = "pedrohjs11"
password = "64IcxNL8vtuMhZ7v"
password_encoded = urllib.parse.quote_plus(password)
uri = f"mongodb+srv://{username}:{password_encoded}@clusterprova.iptxmnu.mongodb.net/?retryWrites=true&w=majority&appName=ClusterProva"

testar_conexao_mongodb(uri)