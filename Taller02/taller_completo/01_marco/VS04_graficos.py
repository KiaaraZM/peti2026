import os, pandas as pd, matplotlib.pyplot as plt

AZUL_UPT, AZUL_EPIS, CIAN = "#16285C", "#174380", "#0EA5E9"

bcrp_path = "evidencias/VS_series_bcrp.csv"
bm_path   = "evidencias/VS_series_banco_mundial.csv"

if not os.path.exists(bcrp_path) or not os.path.exists(bm_path):
    print("Error: Los archivos de evidencias no existen aún.")
    exit(1)

bcrp = pd.read_csv(bcrp_path)
bm   = pd.read_csv(bm_path)

fig, ax = plt.subplots(1, 2, figsize=(14,5))

# Serie nacional: tipo de cambio
tc = bcrp[bcrp.codigo == "PN01207PM"].copy()
ax[0].plot(range(len(tc)), tc.valor, color=AZUL_UPT, linewidth=2)
ax[0].set_title("Tipo de cambio bancario venta (S/ por US$)\nFuente: BCRP", fontsize=11, fontweight="bold")
step = max(1, len(tc)//8)
ax[0].set_xticks(range(0, len(tc), step))
ax[0].set_xticklabels(tc.periodo.iloc[::step], rotation=45, ha="right", fontsize=8)
ax[0].grid(alpha=.3)

# Comparación regional: uso de internet
uso = bm[bm.codigo == "IT.NET.USER.ZS"].copy()
for pais, g in uso.groupby("pais"):
    g = g.sort_values("año")
    ax[1].plot(g["año"], g.valor, marker="o", markersize=3,
               linewidth=2.5 if pais == "Peru" else 1.2,
               color=AZUL_UPT if pais == "Peru" else "#9CA3AF", label=pais)
ax[1].set_title("Personas que usan internet (% de la población)\nFuente: Banco Mundial", fontsize=11, fontweight="bold")
ax[1].legend(fontsize=8); ax[1].grid(alpha=.3); ax[1].set_ylabel("%")

os.makedirs("graficos", exist_ok=True)
plt.tight_layout()
plt.savefig("graficos/VS_contexto.png", dpi=140)
print("Gráfico generado con éxito en: graficos/VS_contexto.png")
