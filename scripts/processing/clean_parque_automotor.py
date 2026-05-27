import pandas as pd
import boto3
from io import StringIO

bucket_name = "proyecto2-jose-anna-datalake"

input_key = "raw/parque_automotor/parque_automotor.csv"
output_key = "trusted/parque_automotor/parque_automotor_limpio.csv"

s3 = boto3.client("s3")

response = s3.get_object(
    Bucket=bucket_name,
    Key=input_key
)

df = pd.read_csv(response["Body"])

print("Dataset original:")
print(df.head())
print(df.shape)

# limpiar nombres de columnas
df.columns = [col.lower() for col in df.columns]

# eliminar nulos
df = df.dropna()

# convertir tipos
numeric_columns = [
    "anio",
    "cantidad_motos",
    "cantidad_carros",
    "cantidad_buses",
    "total_vehiculos"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna()

print("Dataset limpio:")
print(df.head())
print(df.shape)

csv_buffer = StringIO()

df.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=bucket_name,
    Key=output_key,
    Body=csv_buffer.getvalue()
)

print("Parque automotor limpio subido a trusted")
