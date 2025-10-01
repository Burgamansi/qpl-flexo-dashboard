import streamlit as st
import pandas as pd

st.title("📊 Flexografia – Produção QPL")

# Link direto para sua planilha em CSV
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/gviz/tq?tqx=out:csv&gid=603983816"

# Carregar dados
df = pd.read_csv(url)

st.subheader("📑 Tabela de Produção")
st.dataframe(df)

st.subheader("📈 Gráfico - Kg Produzido")
if "Kg Produzido" in df.columns:
    st.line_chart(df["Kg Produzido"])
else:
    st.warning("Coluna 'Kg Produzido' não encontrada na planilha.")
