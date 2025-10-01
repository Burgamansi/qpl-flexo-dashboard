import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

st.title("📊 Flexografia – Produção QPL")

# --- Link da planilha ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# ✅ Ajustar datas no formato PT-BR (ex: '01/set.')
df["Data"] = df["Data"].astype(str).str.replace(".", "", regex=False)  # tira ponto final
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna de mês/ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")  # Setembro/2025

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📊 Produção Diária ({mes_filtro})")

fig, ax = plt.subplots(figsize=(10,5))

# Barras de metragem (convertida para milheiros)
ax.bar(df_daily["Data"], df_daily["Metragem"]/1000, width=0.4, color="orange", label="Metragem (milheiros)")

# Barras de Kg Produzido (escala menor, verde)
ax.bar(df_daily["Data"], df_daily["Kg Produzido"]/1000, width=0.4, color="green", label="Kg Produzido (milheiros eqv.)", alpha=0.7)

ax.set_ylabel("Produção (milheiros)")
ax.set_xlabel("Data")
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)
