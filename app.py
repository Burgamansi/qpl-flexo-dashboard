import streamlit as st
import pandas as pd

st.title("📊 Flexografia – Produção QPL")

# 🔗 Link direto para a planilha Google Sheets (exportar como CSV)
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

# 📥 Carregar dados
df = pd.read_csv(url)

# 🛠️ Corrigir nomes das colunas (remove espaços extras e quebras de linha)
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Mostrar colunas carregadas (debug, pode tirar depois)
st.write("✅ Colunas encontradas:", list(df.columns))

# 📑 Mostrar tabela completa
st.subheader("📑 Tabela de Produção")
st.dataframe(df)

# 📈 Gráfico de Kg Produzido
st.subheader("📈 Gráfico - Kg Produzido")

# Procurar coluna que contenha "Kg Produzido" (ignora maiúsculas/minúsculas)
col_kg = [c for c in df.columns if "kg produzido" in c.lower()]

if col_kg:
    st.line_chart(df[col_kg[0]])
else:
    st.warning("⚠️ Nenhuma coluna com 'Kg Produzido' encontrada na planilha.")
