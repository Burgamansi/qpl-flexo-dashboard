import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="QPL Flexo Dashboard", layout="wide")

# ==========================
# Carregar dados
# ==========================
SHEET_CSV = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

@st.cache_data(ttl=900)
def load_data():
    df = pd.read_csv(SHEET_CSV)

    # Renomear colunas para evitar problemas
    rename_map = {
        "Kg\nProduzido": "Kg Produzido",
        "KgProduzido": "Kg Produzido",
        "Metragem ": "Metragem",
        "Total - Horas": "Total Horas"
    }
    df.rename(columns=rename_map, inplace=True)

    # Normalizar nomes de colunas
    df.columns = [c.strip().replace("\n", " ").replace("  ", " ") for c in df.columns]

    # Converter colunas numéricas
    num_cols = ["Largura", "Kg Produzido", "Metragem", "Gramatura", "Kg Apara"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Converter colunas de data
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date

    # Converter Total Horas em decimal (se existir)
    if "Total Horas" in df.columns:
        def parse_horas(x):
            try:
                h, m = str(x).split(":")
                return int(h) + int(m)/60
            except:
                return 0
        df["Horas (dec)"] = df["Total Horas"].apply(parse_horas)

    return df

df = load_data()

st.title("📊 QPL Flexo Dashboard")

# ==========================
# Resumo dos Indicadores
# ==========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Produção Total (Kg)", f"{df['Kg Produzido'].sum():,.0f}")
with col2:
    st.metric("Horas Totais", f"{df['Horas (dec)'].sum():,.2f}")
with col3:
    eficiencia = df["Kg Produzido"].sum() / df["Horas (dec)"].sum() if df["Horas (dec)"].sum() > 0 else 0
    st.metric("Eficiência Média (Kg/h)", f"{eficiencia:,.2f}")
with col4:
    aproveitamento = 100 * (1 - (df["Kg Apara"].sum() / df["Kg Produzido"].sum())) if df["Kg Produzido"].sum() > 0 else 0
    st.metric("Aproveitamento (%)", f"{aproveitamento:,.2f}")

st.divider()

# ==========================
# Gráfico Produção diária
# ==========================
if "Data" in df.columns and "Kg Produzido" in df.columns and "Metragem" in df.columns:
    st.subheader("📊 Produção diária - Kg (barras) x Metragem (linha)")

    df_day = df.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

    fig = px.bar(df_day, x="Data", y="Kg Produzido", title="Produção diária - Kg e Metragem")
    fig.add_scatter(x=df_day["Data"], y=df_day["Metragem"], mode="lines+markers", name="Metragem")

    fig.update_layout(
        yaxis=dict(title="Kg Produzido"),
        yaxis2=dict(title="Metragem", overlaying="y", side="right"),
        legend=dict(orientation="h", y=-0.3)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Colunas necessárias ('Data', 'Kg Produzido', 'Metragem') não encontradas.")
    st.dataframe(df.head(10))  # DEBUG

st.divider()

# ==========================
# Gráfico Paradas
# ==========================
if "Data" in df.columns and "Horas (dec)" in df.columns:
    st.subheader("⚡ Paradas por Dia (Total de Horas)")

    df_parada = df.groupby("Data")["Horas (dec)"].sum().reset_index()

    fig2 = px.bar(df_parada, x="Data", y="Horas (dec)",
                  title="Total de Horas de Parada por Dia",
                  text_auto=".2f")

    fig2.update_layout(yaxis=dict(title="Horas Totais"))
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ Colunas necessárias ('Data', 'Horas (dec)') não encontradas.")
    st.dataframe(df.head(10))  # DEBUG
