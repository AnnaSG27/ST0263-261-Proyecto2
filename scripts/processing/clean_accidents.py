import pandas as pd
import boto3
from io import BytesIO

bucket_name = "proyecto2-jose-anna-datalake"

input_key = "raw/accidentes/historico_siniestros_bogota_d.c_-.csv"
output_key = "trusted/accidentes/accidentes_limpios.csv"

s3 = boto3.client("s3")

# leer desde S3

response = s3.get_object(

    Bucket=bucket_name,

    Key=input_key

)

df = pd.read_csv(response["Body"])

print("Dataset original:")

print(df.shape)

# convertir fecha

df["FECHA_OCURRENCIA_ACC"] = pd.to_datetime(

    df["FECHA_OCURRENCIA_ACC"],

    errors="coerce"

)

# crear fecha simple para joins

df["FECHA"] = df["FECHA_OCURRENCIA_ACC"].dt.date

# seleccionar columnas útiles

df = df[

    [

        "FECHA_OCURRENCIA_ACC",

        "FECHA",

        "ANO_OCURRENCIA_ACC",

        "GRAVEDAD",

        "CLASE_ACC",

        "LOCALIDAD",

        "LATITUD",

        "LONGITUD"

    ]

]

# eliminar nulos importantes

df = df.dropna(subset=["LOCALIDAD"])

# eliminar fechas inválidas

df = df.dropna(subset=["FECHA_OCURRENCIA_ACC"])

print("Dataset limpio:")

print(df.shape)

# guardar temporalmente

csv_buffer = BytesIO()

df.to_csv(csv_buffer, index=False)

csv_buffer.seek(0)

# subir trusted

s3.put_object(

    Bucket=bucket_name,

    Key=output_key,

    Body=csv_buffer.getvalue()

)

print("Dataset limpio subido a trusted")
