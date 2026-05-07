import boto3
import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when

bucket_name = "proyecto2-jose-anna-datalake"

input_key = "raw/clima/clima_bogota_2024.csv"
output_key = "trusted_spark/clima/clima_bogota_limpio_spark.csv"

local_input = "/home/ubuntu/tmp/clima_raw.csv"
local_output_dir = "/home/ubuntu/tmp/clima_spark_output"

s3 = boto3.client("s3")

os.makedirs("/home/ubuntu/tmp", exist_ok=True)

if os.path.exists(local_output_dir):
    shutil.rmtree(local_output_dir)

print("Descargando clima desde S3 raw...")
s3.download_file(bucket_name, input_key, local_input)

spark = SparkSession.builder \
    .appName("CleanClimaSpark") \
    .getOrCreate()

df = spark.read.option("header", True).option("inferSchema", True).csv(local_input)

print("Dataset original:")
df.printSchema()
print(df.count())

df_clean = df.select(
    to_date(col("fecha")).alias("fecha"),
    col("precipitacion_mm").cast("double").alias("precipitacion_mm"),
    col("temperatura_promedio_c").cast("double").alias("temperatura_promedio_c")
).dropna(subset=["fecha"])

df_clean = df_clean.withColumn(
    "llovio",
    when(col("precipitacion_mm") > 0, True).otherwise(False)
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

print("Subiendo clima procesado con Spark a S3...")
s3.upload_file(part_file, bucket_name, output_key)

spark.stop()

print("ETL Spark de clima finalizado correctamente")