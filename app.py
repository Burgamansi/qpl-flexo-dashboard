import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Flexografia – Produção QPL")

# --- Carregar dados ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"
df = pd.read_csv(url)

# Corrigir nomes de colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Converter coluna Data
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Traduzir meses manualmente
meses_pt = {
    "Jan": "Janeiro", "Feb": "Fevereiro", "Mar": "Março",
    "Apr": "Abril", "May": "Maio", "Jun": "Junho",
    "Jul": "Julho", "Aug": "Agosto", "Sep": "Setembro",
    "Oct": "Outubro", "Nov": "Novembro", "Dec": "Dezembro"
}

# Criar coluna Mes_Ano com meses traduzidos
df["Mes_Ano"] = df["Data"].dt.strftime("%b/%Y")
df["Mes_Ano"] = df["Mes_Ano"].apply(lambda x: x.replace(x.split("/")[0], meses_pt[x.split("/")[0]]))

# --- Filtro lateral ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

# Filtrar
df_filtrado = df[df["Mes_Ano"] == mes_filtro]
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(12,6))

# Barras - Kg Produzido
barras = ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
ax1.set_ylabel("Kg Produzido", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Rótulos formatados com pontos
for b in barras:
    valor = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2, valor + 200, f"{valor:,.0f}".replace(",", "."),
             ha="center", va="bottom", fontsize=8, color="black")

# Linha - Metragem
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
ax2.set_ylabel("Metragem", color="red")
ax2.tick_params(axis="y", labelcolor="red")

plt.xticks(rotation=45)
fig.tight_layout()
st.pyplot(fig)
