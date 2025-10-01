import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Carregar dados ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/gviz/tq?tqx=out:csv&gid=60398316"
df = pd.read_csv(url)

# Corrigir nomes das colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# --- Conversão da coluna Data ---
# Criar dicionário para meses abreviados em português
mapa_meses = {
    "jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05", "jun": "06",
    "jul": "07", "ago": "08", "set": "09", "out": "10", "nov": "11", "dez": "12"
}

# Normalizar strings da coluna Data
df["Data"] = df["Data"].astype(str).str.replace(".", "", regex=False).str.strip()

# Substituir abreviações por números
for mes_pt, mes_num in mapa_meses.items():
    df["Data"] = df["Data"].str.replace(mes_pt, mes_num, regex=False)

# Agora converter para datetime (ano fixo 2025)
df["Data"] = pd.to_datetime(df["Data"] + "/2025", format="%d/%m/%Y", errors="coerce")

# Criar coluna Mês/Ano
df["MesAno"] = df["Data"].dt.strftime("%B/%Y")

# --- Exibir tabela inicial ---
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# --- FILTROS ---
st.sidebar.header("🔎 Filtros")

meses = df["MesAno"].dropna().unique()
mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(meses))

df_filtrado = df[df["MesAno"] == mes_filtro]

opcoes = st.sidebar.multiselect(
    "Selecione métricas para exibir:", 
    ["Kg Produzido", "Metragem"], 
    default=["Kg Produzido","Metragem"]
)

# --- AGRUPAMENTO ---
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- GRÁFICO ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(10,5))

if "Kg Produzido" in opcoes:
    ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
    ax1.set_ylabel("Kg Produzido", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

if "Metragem" in opcoes:
    ax2 = ax1.twinx()
    ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
    ax2.set_ylabel("Metragem", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

plt.xticks(rotation=45, ha="right")
fig.tight_layout()
st.pyplot(fig)
