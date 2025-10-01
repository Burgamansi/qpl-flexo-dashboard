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

# Converter datas (tipo 01/set.)
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna mês/ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")

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
st.subheader("📊 " + f"Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(12,6))
largura_barra = 0.4
x = range(len(df_daily))

# --- Barras (Kg Produzido) ---
bars = ax1.bar(
    [i - largura_barra/2 for i in x],
    df_daily["Kg Produzido"],
    width=largura_barra,
    color="green",
    label="Kg Produzido"
)
ax1.set_ylabel("Kg Produzido", color="green")
ax1.tick_params(axis="y", labelcolor="green")

# Rótulos nas barras (formato 5.000)
for bar in bars:
    height = bar.get_height()
    ax1.annotate(f"{height:,.0f}".replace(",", "."),
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0, 5), textcoords="offset points",
                 ha="center", va="bottom", fontsize=8, color="black")

# --- Barras (Metragem em milhares) ---
bars2 = ax1.bar(
    [i + largura_barra/2 for i in x],
    df_daily["Metragem"]/1000,  # dividir por mil
    width=largura_barra,
    color="orange",
    label="Metragem (milheiros)"
)

# Rótulos nas barras (formato 5.000)
for bar in bars2:
    height = bar.get_height()
    ax1.annotate(f"{height:,.0f}".replace(",", "."),
                 xy=(bar.get_x() + bar.get_width()/2, height),
                 xytext=(0, 5), textcoords="offset points",
                 ha="center", va="bottom", fontsize=8, color="black")

# Eixo X com datas
ax1.set_xticks(list(x))
ax1.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

# Legenda
ax1.legend()

fig.tight_layout()
st.pyplot(fig)
