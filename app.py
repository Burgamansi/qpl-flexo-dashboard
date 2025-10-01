import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da planilha ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# ✅ Ajustar datas do formato '01/set.' para datetime
df["Data"] = (
    df["Data"]
    .astype(str)
    .str.replace(".", "", regex=False)   # remove ponto final
    .str.strip()
)
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna de mês/ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")  # Ex: Setembro/2025

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(df["Mes_Ano"].dropna().unique()))

df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar produção
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📊 Produção Diária ({mes_filtro})")

fig, ax = plt.subplots(figsize=(10,5))

# Barras Metragem (milheiros)
ax.bar(df_daily["Data"], df_daily["Metragem"]/1000, color="orange", label="Metragem (milheiros)", alpha=0.7)

# Barras Kg Produzido (menor, em verde)
ax.bar(df_daily["Data"], df_daily["Kg Produzido"]/1000, color="green", label="Kg Produzido (milheiros eqv.)", alpha=0.7)

# Rótulos e legendas
ax.set_ylabel("Produção (milheiros)")
ax.set_xlabel("Data")
plt.xticks(rotation=45)
ax.legend()

# Adicionar valores no topo das barras
for i, row in df_daily.iterrows():
    ax.text(row["Data"], row["Metragem"]/1000 + 0.2, f'{row["Metragem"]/1000:.1f}', ha='center', fontsize=8, color="orange")
    ax.text(row["Data"], row["Kg Produzido"]/1000 + 0.2, f'{row["Kg Produzido"]/1000:.1f}', ha='center', fontsize=8, color="green")

st.pyplot(fig)

