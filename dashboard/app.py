import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Dashboard de Accidentes Viales en Bogotá")

df = pd.read_csv("datasets/accidentes/accidentes_limpios.csv")

st.subheader("Vista general")
st.write(df.head())

st.metric("Total de accidentes", len(df))
st.metric("Localidades registradas", df["LOCALIDAD"].nunique())

st.subheader("Top 10 localidades con más accidentes")

top_localidades = df["LOCALIDAD"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 5))
top_localidades.plot(kind="bar", ax=ax)
ax.set_xlabel("Localidad")
ax.set_ylabel("Cantidad de accidentes")
ax.set_title("Top 10 localidades con más accidentes")
plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("Accidentes por gravedad")

gravedad = df["GRAVEDAD"].value_counts()

fig2, ax2 = plt.subplots(figsize=(8, 5))
gravedad.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Gravedad")
ax2.set_ylabel("Cantidad")
ax2.set_title("Cantidad de accidentes por gravedad")
plt.xticks(rotation=45)

st.pyplot(fig2)