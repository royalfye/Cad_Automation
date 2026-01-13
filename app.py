import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.organize import organizar_planilha
from src.main import run_full_automation

ROOT_DIR = Path(__file__).resolve().parent
ARQUIVO_OCORRENCIAS = ROOT_DIR / "data" / "chamadas_csv" / "nova_planilha_ocorrencias.xlsx"

@st.cache_data(ttl=300)
def carregar_dados(caminho: Path):
    if not caminho.exists():
        return None
    try:
        df = pd.read_excel(caminho)
        return df
    except Exception as e:
        st.error(f"Erro ao ler Excel: {e}")
        return None

def main():
    st.set_page_config(page_title="Cad Automation", layout="wide", page_icon="🛡️")

    with st.sidebar:
        st.title("🛡️ Sistema CAD")
        from streamlit_option_menu import option_menu
        menu = option_menu(
            "Menu Principal", ["Automação", "Disparos"],
            icons=["gear", "chat-text"], default_index=0
        )

    if menu == "Automação":
        st.header("⚙️ Painel de Controle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Sincronizar e Organizar", use_container_width=True):
                with st.spinner("Robô em ação... Não mexa no mouse!"):
                    sucesso = run_full_automation()
                    
                    if sucesso:
                        st.success("Dados sincronizados e formatados com sucesso!")
                        st.cache_data.clear() 
                        st.rerun()
                    else:
                        st.error("A automação falhou. Verifique se o CAD está visível na tela.")

        st.divider()

        df = carregar_dados(ARQUIVO_OCORRENCIAS)
        if df is not None:
            st.subheader("📋 Últimas Ocorrências")
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info("Nenhum dado encontrado. Clique em Sincronizar.")

if __name__ == "__main__":
    main()