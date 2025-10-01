import streamlit as st
import pandas as pd

st.title("📊 Flexografia – Produção QPL")

# Link da planilha no formato CSV
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# Carregar dados
df = pd.read_csv(url)

# Corrigir nomes das colunas (remove espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Mostrar colunas encontradas
st.write("Colunas corrigidas:", list(df.columns))

# Exibir tabela de produção
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# Exibir gráfico de produção
st.subheader("📈 Gráfico - Kg Produzido")
if "Kg Produzido" in df.columns:
    st.line_chart(df["Kg Produzido"])
else:
    st.warning("Coluna 'Kg Produzido' não encontrada na planilha.")
