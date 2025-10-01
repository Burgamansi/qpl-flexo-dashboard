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

    # Normaliza nomes das colunas
    df.columns = (
        df.columns.str.strip()
        .str.replace("\n", " ")
        .str.replace("  ", " ")
        .str.replace("\xa0", " ")
    )

    # Converte numéricos de forma robusta
    for c in ["Largura", "Kg Produzido", "Metragem", "Gramatura", "Kg Apara"]:
        if c in df.columns:
            df[c] = (
                df[c].astype(str)
                .str.replace(",", ".")
                .str.extract(r"(\d+\.?\d*)")[0]
            )
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Converte Data
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date

    # Converte "Total - Horas" em decimal
    def parse_duration(x):
        try:
            partes = str(x).split(":")
            if len(partes) == 2:  # hh:mm
                h, m = int(partes[0]), int(partes[1])
                return h + m/60
            elif len(partes) == 3:  # hh:mm:ss
                h, m, s = int(partes[0]), int(partes[1]), int(partes[2])
                return h + m/60 + s/3600
            else:
                return pd.to_timedelta(str(x)).total_seconds()/3600
        except:
            return np.nan

    if "Total - Horas" in df.columns:
        df["Horas (dec)"] = df["Total - Horas"].apply(parse_duration)

    return df

# Carregar base
df = load_data()

st.title("📊 QPL Flexo Dashboard")
st.caption(f"Registros carregados: {len(df):,}")

# Debug: listar colunas e exemplos
st.write("📌 Colunas detectadas:", df.columns.tolist())
for col in ["Kg Produzido", "Metragem", "Horas (dec)"]:
    if col in df.columns:
        st.write(f"Exemplo {col}:", df[col].head(10).tolist())

# Preview
st.dataframe(df.head(20), use_container_width=True)

# Criar abas
aba1, aba2, aba3, aba4 = st.tabs(["📌 Resumo", "👷 Operadores", "🏭 Clientes", "⚡ Paradas"])

# ============================
# 📌 Resumo
# ============================
with aba1:
    st.subheader("Resumo dos Indicadores")

    kg_col = "Kg Produzido"
    horas_col = "Horas (dec)"
    apara_col = "Kg Apara"

    col1, col2, col3, col4 = st.columns(4)

    # Produção Total
    with col1:
        if kg_col in df.columns:
            st.metric("Produção Total (Kg)", f"{df[kg_col].sum():,.0f}")

    # Horas Totais
    with col2:
        if horas_col in df.columns:
            st.metric("Horas Totais", f"{df[horas_col].sum():,.2f}")

    # Eficiência
    with col3:
        if kg_col in df.columns and horas_col in df.columns:
            prod = df[kg_col].sum()
            horas = df[horas_col].sum()
            eff = prod / horas if horas > 0 else 0
            st.metric("Eficiência Média (Kg/h)", f"{eff:,.2f}")

    # Aproveitamento
    with col4:
        if kg_col in df.columns and apara_col in df.columns:
            prod = df[kg_col].sum()
            apara = df[apara_col].sum()
            aproveitamento = (prod / (prod + apara) * 100) if (prod + apara) > 0 else 0
            st.metric("Aproveitamento (%)", f"{aproveitamento:,.2f}")

    # Produção diária: barras (Kg) + linha (Metragem)
    if "Data" in df.columns and kg_col in df.columns and "Metragem" in df.columns:
        st.subheader("📊 Produção diária - Kg (barras) x Metragem (linha)")

        df_day = df.groupby("Data")[[kg_col, "Metragem"]].sum().reset_index()

        fig = px.bar(df_day, x="Data", y=kg_col, title="Produção diária - Kg e Metragem")
        fig.add_scatter(x=df_day["Data"], y=df_day["Metragem"], mode="lines+markers",
                        name="Metragem", yaxis="y2")

        fig.update_layout(
            yaxis=dict(title="Kg Produzido"),
            yaxis2=dict(title="Metragem", overlaying="y", side="right"),
            legend=dict(orientation="h", y=-0.3)
        )
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
    if "Data" in df.columns and horas_col in df.columns:
        st.subheader("⚡ Paradas por Dia (Total de Horas)")
        df_parada = df.groupby("Data")[horas_col].sum().reset_index()

        fig2 = px.bar(df_parada, x="Data", y=horas_col,
                      title="Total de Horas de Parada por Dia",
                      text_auto=".2f")
        fig2.update_layout(yaxis=dict(title="Horas Totais"))
        st.plotly_chart(fig2, use_container_width=True)
