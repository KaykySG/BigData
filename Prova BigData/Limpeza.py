import pandas as pd

def verificar_tratamentos(df):
    """Verifica os tratamentos realizados em um DataFrame."""

    print("Verificação dos tratamentos:")

    # Verificar valores ausentes
    if df.isnull().sum().sum() == 0:
        print("- Nenhum valor ausente encontrado.")
    else:
        print("- Valores ausentes ainda presentes.")

    # Verificar duplicatas
    if df.duplicated().sum() == 0:
        print("- Nenhuma linha duplicada encontrada.")
    else:
        print("- Linhas duplicadas ainda presentes.")

    # Verificar padronização de texto (exemplo)
    for coluna in df.select_dtypes(include='object').columns:
        if df[coluna].str.islower().all() and df[coluna].str.strip().equals(df[coluna]):
            print(f"- Coluna '{coluna}' padronizada com sucesso.")
        else:
            print(f"- Coluna '{coluna}' não está totalmente padronizada.")

caminho_arquivo = r"C:\Users\aluno\Documents\GitHub\BigData\Prova BigData\archive\steam.csv"
try:
    df = pd.read_csv(caminho_arquivo)
    verificar_tratamentos(df)
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
