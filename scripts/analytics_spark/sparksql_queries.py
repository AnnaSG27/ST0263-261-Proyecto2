

from pyspark.sql import SparkSession

BUCKET_NAME = "proyecto2-jose-anna-datalake"

ACCIDENTES_PATH = f"s3://{BUCKET_NAME}/trusted_spark/accidentes/"
CLIMA_PATH = f"s3://{BUCKET_NAME}/trusted_spark/clima/"
PARQUE_PATH = f"s3://{BUCKET_NAME}/trusted_spark/parque_automotor/"

OUTPUT_BASE = f"s3://{BUCKET_NAME}/refined/sparksql/"

spark = SparkSession.builder \
    .appName("SparkSQLAnalyticsEMR") \
    .getOrCreate()

print("Leyendo datasets trusted_spark desde S3...")

accidentes_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(ACCIDENTES_PATH)

clima_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(CLIMA_PATH)

parque_df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv(PARQUE_PATH)

print("Registrando vistas temporales SparkSQL...")

accidentes_df.createOrReplaceTempView("accidentes")
clima_df.createOrReplaceTempView("clima")
parque_df.createOrReplaceTempView("parque_automotor")

# QUERY 1
print("Ejecutando Query 1: Top localidades")

q1 = spark.sql("""
    SELECT
        LOCALIDAD AS localidad,
        COUNT(*) AS total_accidentes
    FROM accidentes
    GROUP BY LOCALIDAD
    ORDER BY total_accidentes DESC
    LIMIT 10
""")

q1.show()

q1.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(f"{OUTPUT_BASE}/top_localidades")

# QUERY 2
print("Ejecutando Query 2: Accidentes por gravedad")

q2 = spark.sql("""
    SELECT
        GRAVEDAD AS gravedad,
        COUNT(*) AS cantidad
    FROM accidentes
    GROUP BY GRAVEDAD
    ORDER BY cantidad DESC
""")

q2.show()

q2.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(f"{OUTPUT_BASE}/accidentes_por_gravedad")

# QUERY 3
print("Ejecutando Query 3: Accidentes por año")

q3 = spark.sql("""
    SELECT
        ANO_OCURRENCIA_ACC AS anio,
        COUNT(*) AS total_accidentes
    FROM accidentes
    GROUP BY ANO_OCURRENCIA_ACC
    ORDER BY anio
""")

q3.show()

q3.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(f"{OUTPUT_BASE}/accidentes_por_anio")

# QUERY 4
print("Ejecutando Query 4: Lluvia vs accidentes")

q4 = spark.sql("""
    SELECT
        c.llovio,
        COUNT(*) AS total_accidentes
    FROM accidentes a
    JOIN clima c
        ON a.FECHA = c.fecha
    GROUP BY c.llovio
    ORDER BY c.llovio
""")

q4.show()

q4.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(f"{OUTPUT_BASE}/lluvia_vs_accidentes")

# QUERY 5
print("Ejecutando Query 5: Accidentes por 1000 vehículos")

q5 = spark.sql("""
    SELECT
        p.localidad,
        COUNT(*) AS accidentes,
        p.total_vehiculos,
        ROUND((COUNT(*) * 1000.0 / p.total_vehiculos), 2)
            AS accidentes_por_1000_vehiculos
    FROM accidentes a
    JOIN parque_automotor p
        ON LOWER(a.LOCALIDAD) = LOWER(p.localidad)
    GROUP BY p.localidad, p.total_vehiculos
    ORDER BY accidentes_por_1000_vehiculos DESC
""")

q5.show()

q5.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(f"{OUTPUT_BASE}/accidentes_por_1000_vehiculos")

spark.stop()

print("Consultas SparkSQL ejecutadas correctamente")
print(f"Resultados disponibles en: {OUTPUT_BASE}")