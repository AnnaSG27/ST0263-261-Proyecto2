import boto3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

# Definimos el nombre del bucket y de la carpeta de queries
BUCKET_NAME = "proyecto2-jose-anna-datalake"
REFINED_PREFIX = "refined/sparksql"

s3 = boto3.client("s3")


def find_result_file(prefix: str) -> str:
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=prefix
    )

    contents = response.get("Contents", [])

    for obj in contents:
        key = obj["Key"]
        if key.endswith(".csv") and "/part-" in key:
            return key

    raise FileNotFoundError(f"No se encontró archivo CSV resultado en s3://{BUCKET_NAME}/{prefix}")


def read_spark_result(result_folder: str) -> pd.DataFrame:
    prefix = f"{REFINED_PREFIX}/{result_folder}/"
    key = find_result_file(prefix)

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    return pd.read_csv(BytesIO(response["Body"].read()))


st.title("Dashboard Analítico - Accidentes Viales Bogotá")

st.caption(
    "Resultados generados con SparkSQL sobre Amazon EMR y almacenados en S3 refined/sparksql."
)

# =========================
# RESULTADO 1
# =========================

df_localidades = read_spark_result("top_localidades")

st.subheader("Top 10 localidades con más accidentes")
st.dataframe(df_localidades)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(
    df_localidades["localidad"],
    df_localidades["total_accidentes"]
)
ax.set_xlabel("Localidad")
ax.set_ylabel("Accidentes")
ax.set_title("Top localidades con más accidentes")
plt.xticks(rotation=45)
st.pyplot(fig)

# =========================
# RESULTADO 2
# =========================

df_gravedad = read_spark_result("accidentes_por_gravedad")

st.subheader("Accidentes por gravedad")
st.dataframe(df_gravedad)

fig2, ax2 = plt.subplots(figsize=(8, 5))
ax2.bar(
    df_gravedad["gravedad"],
    df_gravedad["cantidad"]
)
ax2.set_xlabel("Gravedad")
ax2.set_ylabel("Cantidad")
ax2.set_title("Accidentes por gravedad")
plt.xticks(rotation=45)
st.pyplot(fig2)

# =========================
# RESULTADO 3
# =========================

df_lluvia = read_spark_result("lluvia_vs_accidentes")

st.subheader("Accidentes en días lluviosos")
st.dataframe(df_lluvia)

fig3, ax3 = plt.subplots(figsize=(6, 4))
ax3.bar(
    df_lluvia["llovio"].astype(str),
    df_lluvia["total_accidentes"]
)
ax3.set_xlabel("¿Llovió?")
ax3.set_ylabel("Accidentes")
ax3.set_title("Accidentes vs lluvia")
st.pyplot(fig3)

# =========================
# RESULTADO 4
# =========================

df_vehiculos = read_spark_result("accidentes_por_1000_vehiculos")

st.subheader("Accidentes por 1000 vehículos")
st.dataframe(df_vehiculos)

fig4, ax4 = plt.subplots(figsize=(10, 5))
ax4.bar(
    df_vehiculos["localidad"],
    df_vehiculos["accidentes_por_1000_vehiculos"]
)
ax4.set_xlabel("Localidad")
ax4.set_ylabel("Accidentes por 1000 vehículos")
ax4.set_title("Riesgo relativo por localidad")
plt.xticks(rotation=45)
st.pyplot(fig4)
