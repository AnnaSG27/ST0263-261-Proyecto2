from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, when

BUCKET_NAME = "proyecto2-jose-anna-datalake"

INPUT_PATH = f"s3://{BUCKET_NAME}/raw/clima/clima_bogota_2024.csv"
OUTPUT_PATH = f"s3://{BUCKET_NAME}/trusted_spark/clima/"

spark = SparkSession.builder \
    .appName("CleanClimaSparkEMR") \
    .getOrCreate()

print("Leyendo clima desde S3 raw con Spark...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(INPUT_PATH)

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

print("Escribiendo clima limpio en S3 trusted_spark...")

df_clean.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH)

spark.stop()

print("ETL Spark de clima finalizado correctamente")