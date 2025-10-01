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

# Converter a coluna Data corretamente
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")

# Fixar ano
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna Mês/Ano
df["Mes_Ano"] = df["Data"].dt.strftime("%m/%Y")

# --- Filtros ---
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

# Converter Metragem para milheiros (dividir por 1000)
df_daily["Metragem (milheiro)"] = df_daily["Metragem"] / 1000

fig, ax = plt.subplots(figsize=(10,5))

# Barras empilhadas
ax.bar(df_daily["Data"], df_daily["Metragem (milheiro)"], color="orange", label="Metragem (milheiros)")
ax.bar(df_daily["Data"], df_daily["Kg Produzido"]/1000, color="green", label="Kg Produzido (milheiros eqv.)")

# Rótulos e estilo
ax.set_ylabel("Produção (milheiros)", fontsize=12)
ax.set_xlabel("Data", fontsize=12)
ax.set_xticks(df_daily["Data"])
ax.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)
ax.legend()

plt.tight_layout()
st.pyplot(fig)
