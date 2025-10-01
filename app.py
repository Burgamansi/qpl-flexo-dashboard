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

    # Normalizar nomes de colunas
    df.columns = df.columns.str.strip().str.replace("\n", " ")

    # Conversões numéricas
    num_cols = ["Largura", "Kg Produzido", "Metragem", "Gramatura", "Kg Apara"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Datas
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date

    # Converter Total Horas em decimal
    if "Total - Horas" in df.columns:
        def parse_horas(x):
            try:
                h, m = str(x).split(":")
                return int(h) + int(m)/60
            except:
                return 0
        df["Horas (dec)"] = df["Total - Horas"].apply(parse_horas)

    # Criar coluna de paradas
    if "Cód. Parada" in df.columns and "Horas (dec)" in df.columns:
        df["Horas Parada"] = df.apply(
            lambda row: row["Horas (dec)"] if pd.notna(row["Cód. Parada"]) and str(row["Cód. Parada"]).strip() != "" else 0,
            axis=1
        )
    else:
        df["Horas Parada"] = 0

    return df

df = load_data()

# ==========================
# Criar abas
# ==========================
aba1, aba2, aba3, aba4, aba5, aba6, aba7 = st.tabs([
    "📌 Resumo", "👷 Operadores", "🏢 Clientes",
    "📦 Produtos", "🏭 Máquinas", "⚡ Paradas", "📏 Gramatura"
])

# ==========================
# Aba 1 - Resumo
# ==========================
with aba1:
    st.subheader("📌 Resumo dos Indicadores")

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

    st.markdown("### 📊 Produção diária - Kg (barras) e Metragem (linha)")
    if "Data" in df.columns:
        df_day = df.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()
        fig = px.bar(df_day, x="Data", y="Kg Produzido", title="Produção diária")
        fig.add_scatter(x=df_day["Data"], y=df_day["Metragem"], mode="lines+markers", name="Metragem", yaxis="y2")
        fig.update_layout(yaxis=dict(title="Kg Produzido"),
                          yaxis2=dict(title="Metragem", overlaying="y", side="right"))
        st.plotly_chart(fig, use_container_width=True)

# ==========================
# Aba 2 - Operadores
# ==========================
with aba2:
    st.subheader("👷 Produção por Operador")
    if "Nome Operador" in df.columns:
        df_op = df.groupby("Nome Operador")[["Kg Produzido", "Horas (dec)"]].sum().reset_index()
        fig_op = px.bar(df_op, x="Nome Operador", y="Kg Produzido", text_auto=True, title="Kg Produzido por Operador")
        st.plotly_chart(fig_op, use_container_width=True)

# ==========================
# Aba 3 - Clientes
# ==========================
with aba3:
    st.subheader("🏢 Produção por Cliente")
    if "Cliente" in df.columns:
        df_cli = df.groupby("Cliente")[["Kg Produzido", "Metragem"]].sum().reset_index()
        fig_cli = px.bar(df_cli, x="Cliente", y="Kg Produzido", text_auto=True, title="Produção (Kg) por Cliente")
        fig_cli.add_scatter(x=df_cli["Cliente"], y=df_cli["Metragem"], mode="lines+markers", name="Metragem", yaxis="y2")
        fig_cli.update_layout(yaxis=dict(title="Kg Produzido"),
                              yaxis2=dict(title="Metragem", overlaying="y", side="right"))
        st.plotly_chart(fig_cli, use_container_width=True)

# ==========================
# Aba 4 - Produtos
# ==========================
with aba4:
    st.subheader("📦 Produção por Produto")
    if "Produto" in df.columns:
        df_prod = df.groupby("Produto")[["Kg Produzido", "Metragem"]].sum().reset_index()
        fig_prod = px.bar(df_prod, x="Produto", y="Kg Produzido", text_auto=True, title="Produção (Kg) por Produto")
        fig_prod.add_scatter(x=df_prod["Produto"], y=df_prod["Metragem"], mode="lines+markers", name="Metragem", yaxis="y2")
        fig_prod.update_layout(yaxis=dict(title="Kg Produzido"),
                               yaxis2=dict(title="Metragem", overlaying="y", side="right"))
        st.plotly_chart(fig_prod, use_container_width=True)

# ==========================
# Aba 5 - Máquinas
# ==========================
with aba5:
    st.subheader("🏭 Produção por Máquina")
    if "Nº MQ" in df.columns:
        df_mq = df.groupby("Nº MQ")[["Kg Produzido", "Horas (dec)"]].sum().reset_index()
        fig_mq = px.bar(df_mq, x="Nº MQ", y="Kg Produzido", text_auto=True, title="Kg Produzido por Máquina")
        fig_mq.add_scatter(x=df_mq["Nº MQ"], y=df_mq["Horas (dec)"], mode="lines+markers", name="Horas", yaxis="y2")
        fig_mq.update_layout(yaxis=dict(title="Kg Produzido"),
                             yaxis2=dict(title="Horas", overlaying="y", side="right"))
        st.plotly_chart(fig_mq, use_container_width=True)

# ==========================
# Aba 6 - Paradas
# ==========================
with aba6:
    st.subheader("⚡ Paradas por Dia e por Motivo")

    if "Data" in df.columns:
        df_parada = df.groupby("Data")["Horas Parada"].sum().reset_index()
        fig2 = px.bar(df_parada, x="Data", y="Horas Parada",
                      title="Total de Horas de Parada por Dia",
                      text_auto=".2f", color="Horas Parada", color_continuous_scale="Reds")
        st.plotly_chart(fig2, use_container_width=True)

    if "Descrição do Código" in df.columns:
        df_motivo = df.groupby("Descrição do Código")["Horas Parada"].sum().reset_index()
        fig3 = px.bar(df_motivo, x="Descrição do Código", y="Horas Parada",
                      title="Paradas por Motivo", text_auto=True, color="Horas Parada", color_continuous_scale="Reds")
        st.plotly_chart(fig3, use_container_width=True)

# ==========================
# Aba 7 - Gramatura
# ==========================
with aba7:
    st.subheader("📏 Controle de Gramatura")
    if "Data" in df.columns and "Gramatura" in df.columns:
        df_gra = df.groupby("Data")["Gramatura"].mean().reset_index()
        fig4 = px.line(df_gra, x="Data", y="Gramatura", markers=True, title="Gramatura Média por Dia")
        st.plotly_chart(fig4, use_container_width=True)
