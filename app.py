import plotly.express as px

st.markdown("---")
st.header("📊 Dashboard de Produção QPL")

# Criar abas
aba1, aba2, aba3, aba4 = st.tabs(["📌 Resumo", "👷 Operadores", "🏭 Clientes", "⚡ Paradas"])

# ============================
# 📌 Resumo
# ============================
with aba1:
    st.subheader("Indicadores Gerais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Produção Total (Kg)", f"{df.get('Kg Produzido', pd.Series()).sum():,.0f}")
    with col2:
        horas = df.get("Horas (dec)", pd.Series()).sum()
        st.metric("Horas Totais", f"{horas:,.2f}")
    with col3:
        prod = df.get("Kg Produzido", pd.Series()).sum()
        eff = prod / horas if horas and horas > 0 else 0
        st.metric("Eficiência Média (Kg/h)", f"{eff:,.2f}")
    with col4:
        apara = df.get("Kg Apara", pd.Series()).sum()
        aproveitamento = (prod / (prod + apara) * 100) if (prod + apara) > 0 else 0
        st.metric("Aproveitamento (%)", f"{aproveitamento:,.2f}")

    # Produção ao longo do tempo
    if "Data" in df.columns and "Kg Produzido" in df.columns:
        st.subheader("📈 Produção ao longo do tempo")
        df_time = df.groupby("Data")["Kg Produzido"].sum().reset_index()
        fig = px.line(df_time, x="Data", y="Kg Produzido", markers=True, title="Kg produzido por dia")
        st.plotly_chart(fig, use_container_width=True)

# ============================
# 👷 Operadores
# ============================
with aba2:
    if "Nome Operador" in df.columns and "Kg Produzido" in df.columns:
        st.subheader("Produção por Operador")
        fig = px.bar(df, x="Nome Operador", y="Kg Produzido", color="Nome Operador",
                     title="Total produzido por operador", text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

# ============================
# 🏭 Clientes
# ============================
with aba3:
    if "Cliente" in df.columns and "Kg Produzido" in df.columns:
        st.subheader("Produção por Cliente")
        fig = px.pie(df, names="Cliente", values="Kg Produzido", title="Participação por Cliente")
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
