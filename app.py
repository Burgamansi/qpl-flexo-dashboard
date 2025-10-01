import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da sua planilha (exportada como CSV do Google Sheets) ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)

# Corrigir nomes de colunas (tirar espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Converter a coluna "Data" para datetime
df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Criar coluna Mês/Ano para o filtro
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")  # exemplo: September/2025

# --- Filtros na barra lateral ---
st.sidebar.header("🔍 Filtros")

# Filtro por mês
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

# Filtrar o dataframe
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por data e somar Kg Produzido e Metragem
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

# Melhorar layout do eixo X (datas dia a dia)
plt.xticks(rotation=45)
fig.tight_layout()

# Mostrar gráfico no Streamlit
st.pyplot(fig)
