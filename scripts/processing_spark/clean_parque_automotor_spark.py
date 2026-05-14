from pyspark.sql import SparkSession
from pyspark.sql.functions import col

BUCKET_NAME = "proyecto2-jose-anna-datalake"

INPUT_PATH = f"s3://{BUCKET_NAME}/raw/parque_automotor/parque_automotor.csv"
OUTPUT_PATH = f"s3://{BUCKET_NAME}/trusted_spark/parque_automotor/"

spark = SparkSession.builder \
    .appName("CleanParqueAutomotorSparkEMR") \
    .getOrCreate()

print("Leyendo parque automotor desde S3 raw con Spark...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(INPUT_PATH)

print("Dataset original:")
df.printSchema()
print(df.count())

df_clean = df.select(
    col("id").cast("int").alias("id"),
    col("localidad"),
    col("anio").cast("int").alias("anio"),
    col("cantidad_motos").cast("int").alias("cantidad_motos"),
    col("cantidad_carros").cast("int").alias("cantidad_carros"),
    col("cantidad_buses").cast("int").alias("cantidad_buses"),
    col("total_vehiculos").cast("int").alias("total_vehiculos")
).dropna(subset=["localidad"])

print("Dataset limpio:")
df_clean.printSchema()
print(df_clean.count())

print("Escribiendo parque automotor limpio en S3 trusted_spark...")

df_clean.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH)

spark.stop()

print("ETL Spark de parque automotor finalizado correctamente")