import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Produção QPL", layout="wide")

st.title("📊 Dashboard de Produção - Flexografia QPL")

uploaded_file = st.file_uploader("Carregar planilha de produção", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, sep=";", encoding="utf-8")
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📑 Dados Carregados")
    st.dataframe(df, use_container_width=True)

    # --- Produção por Operador ---
    st.subheader("👤 Produção por Operador")
    fig_op = px.bar(df, x="Nome Operador", y="Kg Produzido", text="Kg Produzido", color="Nome Operador")
    fig_op.update_traces(texttemplate='%{text:,.0f}', textposition="outside")
    st.plotly_chart(fig_op, use_container_width=True)

    # --- Produção por Turno ---
    st.subheader("🌙 Produção por Turno")
    fig_turno = px.pie(df, names="Turno", values="Kg Produzido")
    st.plotly_chart(fig_turno, use_container_width=True)

    # --- Códigos de Parada ---
    st.subheader("🛑 Códigos de Parada")
    paradas = df.groupby("Cód. Parada").size().reset_index(name="Qtde")
    fig_paradas = px.bar(paradas, x="Cód. Parada", y="Qtde", text="Qtde", color="Cód. Parada")
    st.plotly_chart(fig_paradas, use_container_width=True)

    # --- Total de Horas ---
    st.subheader("⏱️ Total de Horas")
    if "Total - Horas" in df.columns:
        try:
            total_horas = pd.to_timedelta(df["Total - Horas"]).dt.total_seconds().sum() / 3600
            st.metric("Horas Totais", f"{total_horas:,.2f}".replace(",", "."))
        except:
            st.warning("⚠️ Coluna 'Total - Horas' não está em formato de hora válido.")

else:
    st.info("📂 Faça upload de um arquivo para ver os gráficos.")
