from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, substring

BUCKET_NAME = "proyecto2-jose-anna-datalake"

INPUT_PATH = f"s3://{BUCKET_NAME}/raw/accidentes/historico_siniestros_bogota_d.c_-.csv"
OUTPUT_PATH = f"s3://{BUCKET_NAME}/trusted_spark/accidentes/"

spark = SparkSession.builder \
    .appName("CleanAccidentsSparkEMR") \
    .getOrCreate()

print("Leyendo accidentes desde S3 raw con Spark...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(INPUT_PATH)

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

df_clean = df_clean.dropna(subset=["FECHA"])

print("Dataset limpio:")
df_clean.printSchema()
print(df_clean.count())

print("Escribiendo accidentes limpios en S3 trusted_spark...")

df_clean.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(OUTPUT_PATH)

spark.stop()

print("ETL Spark de accidentes finalizado correctamente")
