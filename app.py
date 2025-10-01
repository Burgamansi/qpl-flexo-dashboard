import plotly.express as px

st.divider()
st.header("📊 Análises Gráficas")

# 1. Produção por Operador
if "Nome Operador" in df.columns and "Kg Produzido" in df.columns:
    st.subheader("Produção por Operador")
    fig1 = px.bar(
        df, 
        x="Nome Operador", 
        y="Kg Produzido", 
        color="Nome Operador",
        title="Total produzido por operador",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2. Produção por Cliente
if "Cliente" in df.columns and "Kg Produzido" in df.columns:
    st.subheader("Produção por Cliente")
    fig2 = px.pie(
        df, 
        names="Cliente", 
        values="Kg Produzido", 
        title="Participação por Cliente"
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3. Produção ao longo do tempo
if "Data" in df.columns and "Kg Produzido" in df.columns:
    st.subheader("Produção ao longo do tempo")
    fig3 = px.line(
        df.groupby("Data")["Kg Produzido"].sum().reset_index(),
        x="Data",
        y="Kg Produzido",
        markers=True,
        title="Kg produzido por dia"
    )
    st.plotly_chart(fig3, use_container_width=True)

# 4. Ranking de Paradas
if "Descrição do Código" in df.columns and "Cód. Parada" in df.columns:
    st.subheader("Códigos de Parada mais Frequentes")
    parada_df = df.groupby("Descrição do Código").size().reset_index(name="Frequência")
    fig4 = px.bar(
        parada_df.sort_values("Frequência", ascending=False),
        x="Descrição do Código",
        y="Frequência",
        title="Top paradas registradas",
        text_auto=True
    )
    st.plotly_chart(fig4, use_container_width=True)
