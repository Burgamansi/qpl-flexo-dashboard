import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

# ---------- CONFIGURAÇÕES ----------
st.set_page_config(layout="wide")
st.title("📊 Flexografia – Produção QPL")

# Forçar meses em português
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except:
    st.warning("⚠️ Locale pt_BR.UTF-8 não disponível, exibindo meses em inglês.")

# ---------- CARREGAR DADOS ----------
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"
df = pd.read_csv(url)

# Corrigir nomes de colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Converter coluna Data
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) else x)

# Criar coluna mês/ano
df["Mes_Ano"] = df["Data"].dt.strftime("%B/%Y").str.capitalize()

# ---------- FILTROS ----------
st.sidebar.header("🔍 Filtros")

meses_disponiveis = df["Mes_Ano"].dropna().unique()
mes_filtro = st.sidebar.selectbox("Selecione o mês", meses_disponiveis)

# Filtrar os dados
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# ---------- TABELA ----------
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# ---------- GRÁFICO ----------
st.subheader(f"📊 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Largura das barras
largura = 0.4
x = range(len(df_daily))

# Barras - Metragem em milheiros
barras1 = ax1.bar([i - largura/2 for i in x], df_daily["Metragem"]/1000, 
                  width=largura, color="orange", label="Metragem (milheiros)")
ax1.set_ylabel("Metragem (milheiros)", color="orange")
ax1.tick_params(axis="y", labelcolor="orange")

# Barras - Kg Produzido
barras2 = ax1.bar([i + largura/2 for i in x], df_daily["Kg Produzido"], 
                  width=largura, color="green", label="Kg Produzido (kg)")
ax1.set_ylabel("Produção (Kg)", color="green")
ax1.tick_params(axis="y", labelcolor="green")

# Rótulos formatados
for b in barras1:
    valor = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2, valor + 0.5, f"{valor:,.0f}".replace(",", "."), 
             ha="center", va="bottom", fontsize=8, color="black")
for b in barras2:
    valor = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2, valor + 0.5, f"{valor:,.0f}".replace(",", "."), 
             ha="center", va="bottom", fontsize=8, color="black")

# Eixo X = Datas
ax1.set_xticks(x)
ax1.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

# Legenda
ax1.legend()

fig.tight_layout()
st.pyplot(fig)
