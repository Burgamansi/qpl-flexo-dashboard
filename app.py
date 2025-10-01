import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="QPL Flexo Dashboard", layout="wide")

# --- Carregar dados ---
SHEET_CSV = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

df = pd.read_csv(SHEET_CSV)

st.title("QPL Flexo Dashboard")
st.dataframe(df.head(20), use_container_width=True)

# --- Dashboard com abas ---
st.markdown("---")
st.header("📊 Dashboard de Produção QPL")

aba1, aba2, aba3, aba4 = st.tabs(["📌 Resumo", "👷 Operadores", "🏭 Clientes", "⚡ Paradas"])

with aba1:
    st.subheader("Resumo")
    st.metric("Produção Total (Kg)", f"{df['Kg Produzido'].sum():,.0f}")

with aba2:
    st.subheader("Produção por Operador")
    fig = px.bar(df, x="Nome Operador", y="Kg Produzido", color="Nome Operador")
    st.plotly_chart(fig, use_container_width=True)
