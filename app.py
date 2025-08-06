import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(layout="wide")
st.title("✈️ Monitor de Passagens Aéreas: BSB ↔ POA")
st.markdown("Atualizado em: " + datetime.now().strftime("%d/%m/%Y %H:%M"))

# Simula dados
def gerar_dados():
    periodos = {
        "18-22 setembro": {
            "IDA": ["2025-09-18", "2025-09-19"],
            "VOLTA": ["2025-09-21", "2025-09-22"]
        },
        "30 out - 03 nov": {
            "IDA": ["2025-10-30", "2025-10-31"],
            "VOLTA": ["2025-11-02", "2025-11-03"]
        },
        "27 nov - 01 dez": {
            "IDA": ["2025-11-27", "2025-11-28"],
            "VOLTA": ["2025-11-30", "2025-12-01"]
        }
    }

    dados = []
    for periodo, direcoes in periodos.items():
        for tipo, datas in direcoes.items():
            for data in datas:
                preco = round(random.uniform(250, 950), 2)
                dados.append({
                    "data_voo": data,
                    "tipo": tipo,
                    "periodo": periodo,
                    "origem": "BSB" if tipo == "IDA" else "POA",
                    "destino": "POA" if tipo == "IDA" else "BSB",
                    "companhia": random.choice(["Latam", "Gol", "Azul"]),
                    "preco": preco,
                    "link": "https://www.google.com/flights"
                })
    return pd.DataFrame(dados)

df_voos = gerar_dados()

# KPIs
st.subheader("📊 Indicadores")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Passagens", len(df_voos))
col2.metric("Preço Médio", f"R$ {df_voos['preco'].mean():.2f}")
col3.metric("Preços < R$ 500", len(df_voos[df_voos['preco'] < 500]))

# Botão de atualização
if st.button("🔄 Atualizar Dados"):
    st.experimental_rerun()

# Mostrar dados por período
for periodo in df_voos["periodo"].unique():
    st.markdown(f"## 🗓️ Período: {periodo}")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🛫 IDA")
        st.dataframe(df_voos[(df_voos["periodo"] == periodo) & (df_voos["tipo"] == "IDA")])
    with col2:
        st.markdown("### 🛬 VOLTA")
        st.dataframe(df_voos[(df_voos["periodo"] == periodo) & (df_voos["tipo"] == "VOLTA")])

# Simula dados por milhas
st.markdown("## 💳 Passagens por Milhas (Azul)")
df_milhas = df_voos.copy()
df_milhas = df_milhas[df_milhas["companhia"] == "Azul"]
df_milhas["milhas"] = df_milhas["preco"].apply(lambda x: int(x * random.uniform(70, 90)))
st.dataframe(df_milhas[["data_voo", "tipo", "periodo", "milhas", "origem", "destino", "link"]])