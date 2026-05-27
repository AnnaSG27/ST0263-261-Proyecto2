import requests
import pandas as pd
import boto3
from io import StringIO

bucket_name = "proyecto2-jose-anna-datalake"

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    "?latitude=4.7110"
    "&longitude=-74.0721"
    "&start_date=2015-01-01"
    "&end_date=2021-09-10"
    "&daily=precipitation_sum,temperature_2m_mean"
    "&timezone=America/Bogota"
)

response = requests.get(url)
response.raise_for_status()

data = response.json()["daily"]

df = pd.DataFrame({
    "fecha": data["time"],
    "precipitacion_mm": data["precipitation_sum"],
    "temperatura_promedio_c": data["temperature_2m_mean"],
})

print(df.head())
print(df.shape)

csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3 = boto3.client("s3")

s3.put_object(
    Bucket=bucket_name,
    Key="raw/clima/clima_bogota_2024.csv",
    Body=csv_buffer.getvalue()
)

print("Clima subido correctamente a S3 raw")
