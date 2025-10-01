import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da planilha ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# ✅ Ajustar datas no formato '01/set.'
df["Data"] = df["Data"].astype(str).str.replace(".", "", regex=False).str.strip()

# Dicionário de meses PT-BR → número
meses_map = {
    "jan": "01", "fev": "02", "mar": "03", "abr": "04",
    "mai": "05", "jun": "06", "jul": "07", "ago": "08",
    "set": "09", "out": "10", "nov": "11", "dez": "12"
}

def converter_data(data_str):
    try:
        dia, mes_abrev = data_str.split("/")
        mes_abrev = mes_abrev.lower()[:3]
        if mes_abrev in meses_map:
            return pd.to_datetime(f"2025-{meses_map[mes_abrev]}-{dia}", format="%Y-%m-%d")
    except:
        return pd.NaT

df["Data"] = df["Data"].apply(converter_data)

# Criar coluna mês/ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(df["Mes_Ano"].dropna().unique()))

df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por Data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📊 Produção Diária ({mes_filtro})")

fig, ax = plt.subplots(figsize=(12,6))

largura_barra = 0.4
x = range(len(df_daily))

# Barras Metragem (milheiros)
ax.bar([i - largura_barra/2 for i in x], df_daily["Metragem"]/1000, 
       width=largura_barra, color="orange", label="Metragem (milheiros)", alpha=0.8)

# Barras Kg Produzido (milheiros equivalentes)
ax.bar([i + largura_barra/2 for i in x], df_daily["Kg Produzido"]/1000, 
       width=largura_barra, color="green", label="Kg Produzido (milheiros eqv.)", alpha=0.8)

# Valores em cima das barras
for i, row in df_daily.iterrows():
    ax.text(i - largura_barra/2, row["Metragem"]/1000 + 0.3, f'{row["Metragem"]/1000:.1f}', 
            ha='center', fontsize=8, color="black", rotation=90)
    ax.text(i + largura_barra/2, row["Kg Produzido"]/1000 + 0.3, f'{row["Kg Produzido"]/1000:.1f}', 
            ha='center', fontsize=8, color="black", rotation=90)

# Eixo X
ax.set_xticks(x)
ax.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

ax.set_ylabel("Produção (milheiros)")
ax.set_xlabel("Data")
ax.legend()
fig.tight_layout()

st.pyplot(fig)
