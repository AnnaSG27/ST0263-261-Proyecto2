import pandas as pd
import boto3
from io import StringIO

bucket_name = "proyecto2-jose-anna-datalake"

input_key = "raw/clima/clima_bogota_2024.csv"
output_key = "trusted/clima/clima_bogota_2024_limpio.csv"

s3 = boto3.client("s3")

response = s3.get_object(
    Bucket=bucket_name,
    Key=input_key
)

df = pd.read_csv(response["Body"])

print("Dataset original:")
print(df.head())
print(df.shape)

df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
df["precipitacion_mm"] = pd.to_numeric(df["precipitacion_mm"], errors="coerce")
df["temperatura_promedio_c"] = pd.to_numeric(df["temperatura_promedio_c"], errors="coerce")

df = df.dropna(subset=["fecha"])

df["llovio"] = df["precipitacion_mm"] > 0

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

print("Clima limpio subido correctamente a S3 trusted")
