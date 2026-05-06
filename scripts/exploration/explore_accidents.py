import pandas as pd

df = pd.read_csv("datasets/accidentes/historico_siniestros_bogota_d.c_-.csv")

print(df.head())

print("\nCOLUMNAS:")
print(df.columns)

print("\nINFO:")
print(df.info())

print("\nNULOS:")
print(df.isnull().sum())