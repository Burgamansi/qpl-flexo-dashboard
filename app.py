# --- Gráfico combinado: Produção Diária ---
import matplotlib.pyplot as plt

st.subheader("📊 Produção Diária: Kg Produzido x Metragem")

# Agrupar por data
df_daily = df.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()

# Criar gráfico
fig, ax1 = plt.subplots(figsize=(10,5))

# Barras para Kg Produzido
ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="skyblue", label="Kg Produzido")
ax1.set_xlabel("Data")
ax1.set_ylabel("Kg Produzido", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Criar eixo secundário para Metragem
ax2 = ax1.twinx()
ax2.plot(df_daily["Data"], df_daily["Metragem"], color="red", marker="o", label="Metragem")
ax2.set_ylabel("Metragem", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Ajustar layout e legendas
fig.tight_layout()
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# Mostrar no Streamlit
st.pyplot(fig)
