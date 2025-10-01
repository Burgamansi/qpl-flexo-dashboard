import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Carregar dados ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/gviz/tq?tqx=out:csv&gid=60398316"
df = pd.read_csv(url)

# Corrigir nomes das colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Garantir que "Data" é realmente data
df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Exibir tabela inicial
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# --- FILTROS ---
st.sidebar.header("🔎 Filtros")
meses = df["Data"].dt.strftime("%B/%Y").unique()
mes_filtro = st.sidebar.selectbox("Selecione o mês", meses)

# Filtrar pelo mês escolhido
df_filtrado = df[df["Data"].dt.strftime("%B/%Y") == mes_filtro]

# Seleção de variáveis
opcoes = st.sidebar.multiselect("Selecione métricas para exibir:", ["Kg Produzido", "Metragem"], default=["Kg Produzido","Metragem"])

# --- AGRUPAMENTO ---
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- GRÁFICO ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(10,5))

# Barras para Kg Produzido (se selecionado)
if "Kg Produzido" in opcoes:
    ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
    ax1.set_ylabel("Kg Produzido", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

# Linha para Metragem (se selecionado)
if "Metragem" in opcoes:
    ax2 = ax1.twinx()
    ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
    ax2.set_ylabel("Metragem", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

# Melhorar formatação do eixo X
plt.xticks(rotation=45, ha="right")

fig.tight_layout()
st.pyplot(fig)
