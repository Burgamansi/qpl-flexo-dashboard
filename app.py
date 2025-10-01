import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da sua planilha em CSV (Google Sheets) ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados, já forçando a coluna Data como datetime ---
df = pd.read_csv(url, parse_dates=["Data"], dayfirst=True)

# Corrigir nomes de colunas (tirar espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Se Data não for datetime, tentar converter
if df["Data"].dtype != "datetime64[ns]":
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Criar coluna Mês/Ano para filtro
df["Mes_Ano"] = df["Data"].dt.strftime("%m/%Y")  # Exemplo: 09/2025

# --- Filtros na barra lateral ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

# Filtrar o dataframe pelo mês escolhido
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por data e somar
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Exibir tabela resumo ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico Produção Diária ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(10,5))

# Barras para Kg Produzido
ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
ax1.set_ylabel("Kg Produzido", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Eixo secundário para Metragem
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
ax2.set_ylabel("Metragem", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Melhorar leitura do eixo X (datas)
plt.xticks(rotation=45)
fig.tight_layout()

st.pyplot(fig)
