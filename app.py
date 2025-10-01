# app.py - QPL Flexo Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="QPL Flexo Dashboard", layout="wide")

# Link direto do Google Sheets como CSV
SHEET_CSV = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

@st.cache_data(ttl=900)
def load_data():
    df = pd.read_csv(SHEET_CSV)

    # Normaliza nomes das colunas (remove espaços extras e quebras de linha)
    df.columns = [c.strip().replace("\n", " ") for c in df.columns]

    # Tenta converter colunas numéricas
    num_cols = ["Largura", "Kg Produzido", "Metragem", "Gramatura", "Kg Apara"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce")

    # Converte datas
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date

    # Converte horas para decimal
    def parse_duration(x):
        try:
            td = pd.to_timedelta(str(x))
            return td.total_seconds()/3600
        except:
            return np.nan

    if "Total - Horas" in df.columns:
        df["Horas (dec)"] = df["Total - Horas"].apply(parse_duration)

    return df

# Carregar base
df = load_data()

st.title("📊 QPL Flexo Dashboard")
st.caption(f"Registros carregados: {len(df):,}")

# Mostrar colunas disponíveis (debug)
st.write("📝 Colunas na base:", df.columns.tolist())

# Preview da base
st.dataframe(df.head(20), use_container_width=True)

# ============================
# Abas
# ============================
aba1, aba2, aba3, aba4 = st.tabs(["📌 Resumo", "👷 Operadores", "🏭 Clientes", "⚡ Paradas"])

# ============================
# 📌 Resumo
# ============================
with aba1:
    st.subheader("Resumo dos Indicadores")

    col1, col2, col3, col4 = st.columns(4)
    kg_col = "Kg Produzido"
    horas_col = "Horas (dec)"
    apara_col = "Kg Apara"

    # Produção total
    with col1:
        if kg_col in df.columns:
            st.metric("Produção Total (Kg)", f"{df[kg_col].sum():,.0f}")
        else:
            st.warning(f"Coluna '{kg_col}' não encontrada.")

    # Horas totais
    with col2:
        if horas_col in df.columns:
            st.metric("Horas Totais", f"{df[horas_col].sum():,.2f}")
        else:
            st.warning(f"Coluna '{horas_col}' não encontrada.")

    # Eficiência
    with col3:
        if kg_col in df.columns and horas_col in df.columns:
            prod = df[kg_col].sum()
            horas = df[horas_col].sum()
            eff = prod / horas if horas > 0 else 0
            st.metric("Eficiência Média (Kg/h)", f"{eff:,.2f}")
        else:
            st.warning("Colunas para eficiência não encontradas.")

    # Aproveitamento
    with col4:
        if kg_col in df.columns and apara_col in df.columns:
            prod = df[kg_col].sum()
            apara = df[apara_col].sum()
            aproveitamento = (prod / (prod + apara) * 100) if (prod + apara) > 0 else 0
            st.metric("Aproveitamento (%)", f"{aproveitamento:,.2f}")
        else:
            st.warning("Colunas para aproveitamento não encontradas.")

    # Produção ao longo do tempo
    if "Data" in df.columns and kg_col in df.columns:
        st.subheader("📈 Produção ao longo do tempo")
        df_time = df.groupby("Data")[kg_col].sum().reset_index()
        fig = px.line(df_time, x="Data", y=kg_col, markers=True, title="Kg produzido por dia")
        st.plotly_chart(fig, use_container_width=True)

# ============================
# 👷 Operadores
# ============================
with aba2:
    if "Nome Operador" in df.columns and kg_col in df.columns:
        st.subheader("Produção por Operador")
        fig = px.bar(df, x="Nome Operador", y=kg_col, color="Nome Operador",
                     title="Total produzido por operador", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

# ============================
# 🏭 Clientes
# ============================
with aba3:
    if "Cliente" in df.columns and kg_col in df.columns:
        st.subheader("Produção por Cliente")
        fig = px.pie(df, names="Cliente", values=kg_col, title="Participação por Cliente")
        st.plotly_chart(fig, use_container_width=True)

# ============================
# ⚡ Paradas
# ============================
with aba4:
    if "Descrição do Código" in df.columns:
        st.subheader("Códigos de Parada mais Frequentes")
        parada_df = df.groupby("Descrição do Código").size().reset_index(name="Frequência")
        parada_df = parada_df.sort_values("Frequência", ascending=False).head(10)
        fig = px.bar(parada_df, x="Descrição do Código", y="Frequência",
                     title="Top paradas registradas", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
