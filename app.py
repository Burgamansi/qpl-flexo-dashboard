# --- Filtros ---
st.sidebar.header("🔍 Filtros")
mes_filtro = st.sidebar.selectbox("Selecione o mês", df["Mes_Ano"].dropna().unique())

# Criar df filtrado
df_filtrado = df[df["Mes_Ano"] == mes_filtro]

# Agrupar por Data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()
df_daily["Metragem_milheiros"] = df_daily["Metragem"] / 1000

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
if not df_filtrado.empty:
    st.subheader(f"📈 Produção Diária ({mes_filtro})")

    fig, ax1 = plt.subplots(figsize=(12,6))

    # Barras (Kg Produzido)
    barras = ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="seagreen", label="Kg Produzido")
    ax1.set_ylabel("Kg Produzido (kg)", color="seagreen")

    # Rótulos das barras
    for b in barras:
        valor = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, valor + 200,
                 f"{valor:,.0f}".replace(",", "."),
                 ha="center", va="bottom", fontsize=8, color="black")

    # Linha (Metragem em milheiros)
    ax2 = ax1.twinx()
    ax2.plot(df_daily["Data"], df_daily["Metragem_milheiros"], color="darkorange", marker="o", linewidth=2, label="Metragem (milheiros)")
    ax2.set_ylabel("Metragem (milheiros)", color="darkorange")

    for x, y in zip(df_daily["Data"], df_daily["Metragem_milheiros"]):
        ax2.text(x, y + 0.3, f"{y:,.1f}".replace(",", "."),
                 ha="center", fontsize=8, color="darkorange")

    plt.xticks(rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
else:
    st.warning("⚠️ Nenhum dado encontrado para exibir no gráfico.")
