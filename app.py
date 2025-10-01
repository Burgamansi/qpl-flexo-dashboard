import matplotlib.dates as mdates

# --- GRÁFICO ---
st.subheader(f"📈 Produção Diária ({mes_filtro})")

fig, ax1 = plt.subplots(figsize=(10,5))

if "Kg Produzido" in opcoes:
    ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
    ax1.set_ylabel("Kg Produzido", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

if "Metragem" in opcoes:
    ax2 = ax1.twinx()
    ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
    ax2.set_ylabel("Metragem", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

# ✅ Ajustar o formato das datas (dia/mês)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))

plt.xticks(rotation=45, ha="right")
fig.tight_layout()
st.pyplot(fig)
