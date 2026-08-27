import sys, requests, pandas as pd, os
from datetime import date

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DESDE_ANIO, HASTA_ANIO = date.today().year - 10, date.today().year

IND = {
    "IT.NET.USER.ZS":  "Personas que usan internet (% de la población)",
    "IT.CEL.SETS.P2":  "Suscripciones a telefonía móvil (por cada 100 personas)",
    "NY.GDP.PCAP.CD":  "PBI per cápita (US$ a precios actuales)",
    "GB.XPD.RSDV.GD.ZS": "Gasto en investigación y desarrollo (% del PBI)",
}
PAISES = "PER;CHL;COL;MEX;BRA"     # comparación regional

frames = []
for cod, nombre in IND.items():
    url = (f"https://api.worldbank.org/v2/country/{PAISES}/indicator/{cod}"
           f"?format=json&date={DESDE_ANIO}:{HASTA_ANIO}&per_page=500")
    try:
        r = requests.get(url, timeout=30); r.raise_for_status()
        payload = r.json()
        if len(payload) < 2 or not payload[1]:
            print(f"[FAIL] {cod}: sin datos"); continue
        df = pd.DataFrame([{"pais": x["country"]["value"], "año": int(x["date"]),
                            "valor": x["value"]} for x in payload[1]])
        df["indicador"] = nombre; df["codigo"] = cod; df["url_origen"] = url
        df["fecha_descarga"] = date.today().isoformat()
        frames.append(df)
        print(f"[OK] {cod}: {len(df)} observaciones")
    except Exception as e:
        print(f"[FAIL] {cod}: {e}")

if frames:
    bm = pd.concat(frames, ignore_index=True).dropna(subset=["valor"])
    os.makedirs("evidencias", exist_ok=True)
    bm.to_csv("evidencias/VS_series_banco_mundial.csv", index=False)
    print("Saved to evidencias/VS_series_banco_mundial.csv")

    ult = bm.sort_values("año").groupby(["indicador","pais"]).last().reset_index()
    print(ult.pivot(index="indicador", columns="pais", values="valor").round(1).to_string())
