# app.py (Etapa 01 - Opção A: CSV público)
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="QPL Flexo Dashboard", layout="wide")

SHEET_CSV = "https://docs.google.com/spreadsheets/d/1q1TJlJAdGBwX_l2KKKzuSisYbibJht6GwKAT9D7X9dY/export?format=csv"

@st.cache_data(ttl=900)  # cache por 15 min
def load_data():
    df = pd.read_csv(SHEET_CSV)
    # Normalizações de nomes de colunas
    df.columns = [c.strip().replace("\n", " ").replace("  ", " ") for c in df.columns]
    # Coerções numéricas (troca vírgula por ponto)
    num_cols = ["Largura","Kg Produzido","Metragem","Gramatura","Kg Apara"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "."), errors="coerce")
    # Datas
    if "Data" in df.columns:
        df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.date
    # Duração (Total - Horas) -> horas decimais
    def parse_duration(x):
        s = str(x)
        if "1899" in s:  # casos vindos do Excel como datetime
            t = pd.to_datetime(s, errors="coerce")
            if pd.notnull(t):
                return (t.hour*3600 + t.minute*60 + t.second)/3600
            return np.nan
        # tenta hh:mm:ss
        try:
            td = pd.to_timedelta(s)
            return td.total_seconds()/3600
        except:
            return np.nan
    if "Total - Horas" in df.columns:
        df["Horas (dec)"] = df["Total - Horas"].apply(parse_duration)
    return df

st.title("QPL Flexo Dashboard — Etapa 01")
df = load_data()
st.caption(f"Registros carregados: {len(df):,}")

# KPIs básicos
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

st.divider()
st.subheader("Pré-visualização da base (topo)")
st.dataframe(df.head(50), use_container_width=True)
