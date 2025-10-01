import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Flexografia – Produção QPL")

# --- Carregar dados ---
url = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"
df = pd.read_csv(url)

# Corrigir nomes de colunas
df.columns = df.columns.str.strip().str.replace("\n", " ", regex=True)

# --- Conversão robusta da coluna Data ---
def parse_date(x):
    for fmt in ["%d/%m/%Y", "%d/%m/%y", "%d/%b", "%d-%m-%Y", "%d.%m.%Y"]:
        try:
            d = pd.to_datetime(x, format=fmt)
            # Se veio sem ano, forçar 2025
            if d.dt.year.iloc[0] == 1900:
                d = d + pd.DateOffset(years=(2025-1900))
            return d
        except:
            pass
    return pd.NaT

df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
df["Data"] = df["Data"].apply(lambda x: x.replace(year=2025) if pd.notnull(x) and x.year < 2025 else x)

# --- Criar coluna Mes_Ano ---
meses_pt = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}
df["Mes_Ano"] = df["Data"].dt.month.map(meses_pt) + "/" + df["Data"].dt.year.astype(str)

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
if df["Mes_Ano"].notna().any():
    mes_filtro = st.sidebar.selectbox("Selecione o mês", sorted(df["Mes_Ano"].dropna().unique()))
    df_filtrado = df[df["Mes_Ano"] == mes_filtro]
else:
    st.sidebar.warning("⚠️ Nenhuma data válida encontrada na planilha.")
    df_filtrado = df.copy()

# Agrupar por Data
df_daily = df_filtrado.groupby("Data")[["Kg Produzido", "Metragem"]].sum().reset_index()
df_daily["Metragem_milheiros"] = df_daily["Metragem"] / 1000

# --- Tabela ---
st.subheader("📋 Tabela de Produção (dados filtrados)")
st.dataframe(df_filtrado)

# --- Gráfico ---
st.subheader(f"📈 Produção Diária ({mes_filtro if not df_filtrado.empty else 'Sem dados'})")

if not df_daily.empty:
    fig, ax1 = plt.subplots(figsize=(12,6))

    barras = ax1.bar(df_daily["Data"], df_daily["Kg Produzido"], color="seagreen", label="Kg Produzido")
    ax1.set_ylabel("Kg Produzido (kg)", color="seagreen")

    for b in barras:
        valor = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, valor + 200, f"{valor:,.0f}".replace(",", "."),
                 ha="center", va="bottom", fontsize=8, color="black")

    ax2 = ax1.twinx()
    ax2.plot(df_daily["Data"], df_daily["Metragem_milheiros"], color="darkorange", marker="o", linewidth=2, label="Metragem (milheiros)")
    ax2.set_ylabel("Metragem (milheiros)", color="darkorange")

    for x, y in zip(df_daily["Data"], df_daily["Metragem_milheiros"]):
        ax2.text(x, y + 0.3, f"{y:,.1f}".replace(",", "."), ha="center", fontsize=8, color="darkorange")

    plt.xticks(rotation=45)
    fig.tight_layout()
    st.pyplot(fig)
else:
    st.warning("⚠️ Nenhum dado encontrado para exibir no gráfico.")
