import boto3
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, substring

bucket_name = "proyecto2-jose-anna-datalake"

input_key = "raw/accidentes/historico_siniestros_bogota_d.c_-.csv"
output_key = "trusted_spark/accidentes/accidentes_limpios_spark.csv"

local_input = "/home/ubuntu/tmp/accidentes_raw.csv"
local_output_dir = "/home/ubuntu/tmp/accidentes_spark_output"

s3 = boto3.client("s3")

os.makedirs("/home/ubuntu/tmp", exist_ok=True)

print("Descargando archivo desde S3 raw...")
s3.download_file(bucket_name, input_key, local_input)

spark = SparkSession.builder \
    .appName("CleanAccidentsSpark") \
    .getOrCreate()

print("Leyendo CSV con Spark...")
df = spark.read.option("header", True).option("inferSchema", True).csv(local_input)

print("Dataset original:")
df.printSchema()
print(df.count())

df_clean = df.select(
    col("FECHA_OCURRENCIA_ACC"),
    col("ANO_OCURRENCIA_ACC"),
    col("GRAVEDAD"),
    col("CLASE_ACC"),
    col("LOCALIDAD"),
    col("LATITUD"),
    col("LONGITUD")
).dropna(subset=["LOCALIDAD", "FECHA_OCURRENCIA_ACC"])

df_clean = df_clean.withColumn(
    "FECHA",
    to_date(
	substring(col("FECHA_OCURRENCIA_ACC"), 1, 10),
	"yyyy/MM/dd"
    )
)

print("Dataset limpio:")
df_clean.printSchema()
print(df_clean.count())

df_clean.coalesce(1).write.mode("overwrite").option("header", True).csv(local_output_dir)

part_file = None
for file in os.listdir(local_output_dir):
    if file.startswith("part-") and file.endswith(".csv"):
        part_file = os.path.join(local_output_dir, file)
        break

if part_file is None:
    raise Exception("No se encontró archivo CSV generado por Spark")

print("Subiendo resultado Spark a S3 trusted_spark...")
s3.upload_file(part_file, bucket_name, output_key)

spark.stop()

print("ETL Spark finalizado correctamente")
