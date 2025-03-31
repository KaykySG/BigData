import pandas as pd

csv_path = r"archive\steam.csv"

df = pd.read_csv(csv_path)

df.head()
df.info()
df.describe()

colunas_com_nulos = df.isnull().sum()

colunas_com_nulos = colunas_com_nulos[colunas_com_nulos > 0]

print("Colunas com valores nulos:")
print(colunas_com_nulos)