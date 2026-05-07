import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pyathena import connect

S3_STAGING_DIR = "s3://proyecto2-jose-anna-datalake/athena-results/"
REGION = "us-east-1"
DATABASE = "movilidad_db"

conn = connect(
    s3_staging_dir=S3_STAGING_DIR,
    region_name=REGION,
    schema_name=DATABASE
)

def run_query(query):
    return pd.read_sql(query, conn)

st.title("Dashboard Analítico - Accidentes Viales Bogotá")

# =========================
# QUERY 1
# =========================

query_localidades = """
SELECT localidad, COUNT(*) AS total_accidentes
FROM movilidad_db.accidentes_limpios
GROUP BY localidad
ORDER BY total_accidentes DESC
LIMIT 10
"""

df_localidades = run_query(query_localidades)

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
# QUERY 2
# =========================

query_gravedad = """
SELECT gravedad, COUNT(*) AS cantidad
FROM movilidad_db.accidentes_limpios
GROUP BY gravedad
ORDER BY cantidad DESC
"""

df_gravedad = run_query(query_gravedad)

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
# QUERY 3
# =========================

query_lluvia = """
SELECT
    c.llovio,
    COUNT(*) AS total_accidentes
FROM movilidad_db.accidentes_limpios a
JOIN movilidad_db.clima_limpio c
    ON a.fecha = c.fecha
GROUP BY c.llovio
"""

df_lluvia = run_query(query_lluvia)

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
# QUERY 4
# =========================

query_vehiculos = """
SELECT
    p.localidad,
    COUNT(*) AS accidentes,
    p.total_vehiculos,
    ROUND(
        (COUNT(*) * 1000.0 / p.total_vehiculos),
        2
    ) AS accidentes_por_1000_vehiculos
FROM movilidad_db.accidentes_limpios a
JOIN movilidad_db.parque_automotor_limpio p
    ON LOWER(a.localidad) = LOWER(p.localidad)
GROUP BY p.localidad, p.total_vehiculos
ORDER BY accidentes_por_1000_vehiculos DESC
"""

df_vehiculos = run_query(query_vehiculos)

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
