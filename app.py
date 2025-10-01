import streamlit as st
import pandas as pd
import plotly.express as px

# --- Carregar dados ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"
df = pd.read_csv(url)

# Corrigir nomes
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# Converter datas
df["Data"] = pd.to_datetime(df["Data"], format="%d/%b", errors="coerce")
df["Mes_Ano"] = df["Data"].dt.strftime("%m/%Y")

# --- Barra lateral ---
st.sidebar.header("🔍 Filtros")
turno = st.sidebar.multiselect("Selecione o turno:", df["Turno"].unique())
operador = st.sidebar.multiselect("Selecione o operador:", df["Nome Operador"].unique())
mes = st.sidebar.selectbox("Selecione o mês:", df["Mes_Ano"].dropna().unique())

# --- Filtrar dados ---
df_filtrado = df.copy()
if turno:
    df_filtrado = df_filtrado[df_filtrado["Turno"].isin(turno)]
if operador:
    df_filtrado = df_filtrado[df_filtrado["Nome Operador"].isin(operador)]
if mes:
    df_filtrado = df_filtrado[df_filtrado["Mes_Ano"] == mes]

# --- Indicadores principais ---
total_horas = df_filtrado["Total - Horas"].sum()
total_paradas = df_filtrado["Cód. Parada"].count()
media_horas = df_filtrado.groupby("Nome Operador")["Total - Horas"].sum().mean()

col1, col2, col3 = st.columns(3)
col1.metric("⏱️ Total de Horas", f"{total_horas:,.0f}")
col2.metric("⚠️ Nº Paradas", f"{total_paradas}")
col3.metric("📊 Média Horas por Operador", f"{media_horas:,.1f}")

# --- Gráficos ---
st.subheader("📊 Horas Totais por Operador")
fig1 = px.bar(df_filtrado.groupby("Nome Operador")["Total - Horas"].sum().reset_index(),
              x="Nome Operador", y="Total - Horas", color="Nome Operador", text="Total - Horas")
st.plotly_chart(fig1)

st.subheader("📊 Distribuição de Códigos de Paradas")
fig2 = px.pie(df_filtrado, names="Cód. Parada", title="Códigos de Paradas (%)")
st.plotly_chart(fig2)

st.subheader("📈 Evolução de Horas por Dia")
fig3 = px.line(df_filtrado.groupby("Data")["Total - Horas"].sum().reset_index(),
               x="Data", y="Total - Horas", markers=True)
st.plotly_chart(fig3)

# --- Tabela resumo ---
st.subheader("📋 Resumo por Operador e Turno")
tabela = df_filtrado.groupby(["Nome Operador", "Turno"]).agg({
    "Total - Horas": "sum",
    "Cód. Parada": "count"
}).reset_index().rename(columns={"Cód. Parada": "Nº Paradas"})

st.dataframe(tabela)
