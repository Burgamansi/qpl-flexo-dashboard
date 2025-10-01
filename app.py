import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Flexografia – Produção QPL")

# Link direto para sua planilha em CSV
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/gviz/tq?tqx=out:csv&gid=60398316"

# --- Carregar dados ---
df = pd.read_csv(url)

# Corrigir nomes das colunas (remove espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Exibir colunas para conferência
st.write("✅ Colunas encontradas:", list(df.columns))

# --- Tabela de Produção ---
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# --- Gráfico de Produção Diária (Kg Produzido x Metragem) ---
st.subheader("📈 Produção Diária: Kg Produzido x Metragem")

# Agrupar por data e somar
df_daily = df.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# Exibir resumo
st.write("Resumo diário:", df_daily)

# Criar gráfico combinado
fig, ax1 = plt.subplots(figsize=(10,5))

# Barras para Kg Produzido
ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
ax1.set_xlabel("Data")
ax1.set_ylabel("Kg Produzido", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Linha para Metragem
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
ax2.set_ylabel("Metragem", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Legendas
fig.tight_layout()
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# Mostrar no Streamlit
st.pyplot(fig)
