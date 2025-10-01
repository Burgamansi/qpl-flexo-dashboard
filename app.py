import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da sua planilha ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)

# Corrigir nomes de colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# 🔑 Converter a coluna Data corretamente
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")

# Fixar ano (2025)
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna Mês/Ano
df["Mes_Ano"] = df["Data"].dt.strftime("%m/%Y")

# --- Filtros na barra lateral ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

# Filtrar
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por Data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Mostrar tabela filtrada ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(10,5))

# Barras (Kg Produzido)
ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
ax1.set_ylabel("Kg Produzido", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Linha (Metragem)
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", linestyle="-", linewidth=2, label="Metragem")
ax2.set_ylabel("Metragem", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Melhorar eixo X
ax1.set_xticks(df_daily["Data"])
ax1.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

# Legendas
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.tight_layout()
st.pyplot(fig)
