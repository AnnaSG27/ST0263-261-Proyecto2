import pandas as pd
from sqlalchemy import create_engine
import boto3

# conexión MariaDB
engine = create_engine(
    "mysql+pymysql://etl_user:etl_password@localhost/movilidad_db"
)

# leer tabla
df = pd.read_sql("SELECT * FROM parque_automotor", engine)

print(df)

# guardar csv temporal
csv_file = "parque_automotor.csv"

df.to_csv(csv_file, index=False)

# subir a S3
s3 = boto3.client("s3")

bucket_name = "proyecto2-jose-anna-datalake"

s3.upload_file(
    csv_file,
    bucket_name,
    "raw/parque_automotor/parque_automotor.csv"
)

print("Archivo subido correctamente a S3")
