import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# --- Link da planilha ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# --- Carregar dados ---
df = pd.read_csv(url)

# Corrigir nomes das colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Converter coluna Data (exemplo: '01/set.') -> datetime
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b.", errors="coerce")

# Fixar ano como 2025
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna Mês/Ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y")  # Exemplo: "Setembro/2025"

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(df["Mes_Ano"].dropna().unique()))

# Filtrar dados
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por Data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# Converter Metragem em milheiros
df_daily["Metragem (milheiro)"] = df_daily["Metragem"] / 1000

# --- Tabela filtrada ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax = plt.subplots(figsize=(12,6))

# Barras lado a lado
largura = 0.4
x = range(len(df_daily))

ax.bar([i - largura/2 for i in x], df_daily["Metragem (milheiro)"], 
       width=largura, color="orange", label="Metragem (milheiros)")

ax.bar([i + largura/2 for i in x], df_daily["Kg Produzido"], 
       width=largura, color="green", label="Kg Produzido (kg)")

# Rótulos nos eixos
ax.set_ylabel("Produção", fontsize=12)
ax.set_xlabel("Data", fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

# Rótulos nos valores
for i, v in enumerate(df_daily["Metragem (milheiro)"]):
    ax.text(i - largura/2, v + 50, f"{v:.1f}", ha="center", fontsize=8, color="black")
for i, v in enumerate(df_daily["Kg Produzido"]):
    ax.text(i + largura/2, v + 50, f"{v:.0f}", ha="center", fontsize=8, color="black")

ax.legend()
plt.tight_layout()
st.pyplot(fig)
