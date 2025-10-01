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

# --- Converter coluna Data ---
df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

# Adicionar ano fixo caso venha sem ano
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Tradução manual de meses
meses_pt = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# Criar coluna Mes_Ano em PT-BR
df["Mes_Ano"] = df["Data"].dt.month.map(meses_pt) + "/" + df["Data"].dt.year.astype(str)

# --- Barra lateral ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(df["Mes_Ano"].dropna().unique()))

# Filtrar dados
df_filtrado = df[df["Mes_Ano"] == mes_filtro]
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# Converter metragem para milheiros
df_daily["Metragem_milheiros"] = df_daily["Metragem"] / 1000

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(12,6))

# Barras - Kg Produzido
barras = ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="seagreen", label="Kg Produzido")
ax1.set_ylabel("Kg Produzido (kg)", color="seagreen")
ax1.tick_params(axis="y", labelcolor="seagreen")

# Rótulos das barras formatados com pontos (5.000 etc.)
for b in barras:
    valor = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2, valor + 200, f"{valor:,.0f}".replace(",", "."),
             ha="center", va="bottom", fontsize=8, color="black")

# Linha - Metragem em milheiros
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem_milheiros"], color="darkorange", marker="o", linewidth=2, label="Metragem (milheiros)")
ax2.set_ylabel("Metragem (milheiros)", color="darkorange")
ax2.tick_params(axis="y", labelcolor="darkorange")

# Rótulos da linha
for x, y in zip(df_daily["Data"], df_daily["Metragem_milheiros"]):
    ax2.text(x, y + 0.3, f"{y:,.1f}".replace(",", "."), ha="center", fontsize=8, color="darkorange")

plt.xticks(rotation=45)
fig.tight_layout()
st.pyplot(fig)
