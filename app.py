# Criar colunas de paradas
if "Cód. Parada" in df.columns and "Horas (dec)" in df.columns:
    # Marca 0 se não tem parada
    df["Horas Parada"] = np.where(df["Cód. Parada"].notna(), df["Horas (dec)"], 0)
else:
    df["Horas Parada"] = 0

# ==========================
# Aba 4 - Paradas
# ==========================
with aba4:
    st.subheader("⚡ Paradas por Dia (Total de Horas)")

    if "Data" in df.columns:
        df_parada = df.groupby("Data")["Horas Parada"].sum().reset_index()

        fig2 = px.bar(
            df_parada, x="Data", y="Horas Parada",
            title="Total de Horas de Parada por Dia",
            text_auto=".2f", color="Horas Parada", color_continuous_scale="Reds"
        )

        fig2.update_layout(yaxis=dict(title="Horas de Parada"))
        st.plotly_chart(fig2, use_container_width=True)
