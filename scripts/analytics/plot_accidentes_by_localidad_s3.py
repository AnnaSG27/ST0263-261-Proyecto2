import boto3
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

bucket_name = "proyecto2-jose-anna-datalake"

file_key = "trusted/accidentes/accidentes_limpios.csv"

s3 = boto3.client("s3")

response = s3.get_object(
    Bucket=bucket_name,
    Key=file_key
)

df = pd.read_csv(response["Body"])

top_localidades = (
    df["LOCALIDAD"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(12,6))

top_localidades.plot(kind="bar")

plt.title("Top 10 localidades con más accidentes")
plt.xlabel("Localidad")
plt.ylabel("Cantidad accidentes")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("evidencias/graphics/top_localidades.png")

plt.show()