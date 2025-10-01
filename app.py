import streamlit as st
import pandas as pd

st.title("📊 Flexografia – Produção QPL")

# 🔗 Link direto para a planilha Google Sheets (CSV export)
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# 📥 Carregar dados
df = pd.read_csv(url)

# 🛠️ Corrigir nomes das colunas (remove espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# 📑 Mostrar tabela completa
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# --- 📈 Gráfico de Produção Diária (Kg Produzido x Metragem) ---
st.subheader("📈 Produção Diária: Kg Produzido x Metragem")

# Agrupar por Data e somar
if "Data" in df.columns and "Kg Produzido" in df.columns and "Metragem" in df.columns:
    df_daily = df.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

    # Mostrar tabela resumo
    st.write("Resumo diário:", df_daily)

    # Gráfico de linhas
    st.line_chart(df_daily.set_index("Data")[["Kg Produzido", "Metragem"]])
else:
    st.warning("⚠️ Verifique se as colunas 'Data', 'Kg Produzido' e 'Metragem' existem na planilha.")

