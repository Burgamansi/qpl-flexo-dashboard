# --- Gráfico ---
st.subheader(f"📊 Produção Diária ({mes_filtro})")

fig, ax = plt.subplots(figsize=(12,6))

largura_barra = 0.4
x = range(len(df_daily))

# Barras Metragem (milheiros)
ax.bar([i - largura_barra/2 for i in x], df_daily["Metragem"]/1000, 
       width=largura_barra, color="orange", label="Metragem (milheiros)", alpha=0.8)

# Barras Kg Produzido (milheiros equivalentes)
ax.bar([i + largura_barra/2 for i in x], df_daily["Kg Produzido"]/1000, 
       width=largura_barra, color="green", label="Kg Produzido (milheiros eqv.)", alpha=0.8)

# ✅ Valores em cima das barras com formatação tipo 5.000
for i, row in df_daily.iterrows():
    ax.text(i - largura_barra/2, (row["Metragem"]/1000) + 0.3, 
            f'{row["Metragem"]/1000:,.0f}'.replace(",", "."), 
            ha='center', fontsize=9, color="black", rotation=90)
    
    ax.text(i + largura_barra/2, (row["Kg Produzido"]/1000) + 0.3, 
            f'{row["Kg Produzido"]/1000:,.0f}'.replace(",", "."), 
            ha='center', fontsize=9, color="black", rotation=90)

# Eixo X
ax.set_xticks(x)
ax.set_xticklabels(df_daily["Data"].dt.strftime("%d/%m"), rotation=45)

ax.set_ylabel("Produção (milheiros)")
ax.set_xlabel("Data")
ax.legend()
fig.tight_layout()

st.pyplot(fig)
