import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "datasets/accidentes/accidentes_limpios.csv"
)

top_localidades = (
    df["LOCALIDAD"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(12,6))

top_localidades.plot(kind="bar")

plt.title("Top 10 localidades con más accidentes")
plt.xlabel("Localidad")
plt.ylabel("Cantidad accidentes")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("top_localidades.png")

plt.show()