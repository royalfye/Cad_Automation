import streamlit as st
import subprocess
import sys
import pandas as pd
from datetime import datetime, time as dttime, timedelta
from streamlit_option_menu import option_menu
from pathlib import Path

# =================================================================
# 1. CONFIGURAÇÃO DE AMBIENTE E CAMINHOS
# =================================================================

# ROOT_DIR identifica a pasta principal "Cad_Automation"
ROOT_DIR = Path(__file__).resolve().parent

# Mapeamento da estrutura de pastas baseada na sua árvore de diretórios
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
CHAMADAS_DIR = DATA_DIR / "chamadas_csv"
SRC_DIR = ROOT_DIR / "src"

# O arquivo real que aparece na sua estrutura é .csv
ARQUIVO_OCORRENCIAS = CHAMADAS_DIR / "nova_planilha_ocorrencias.xlsx"

# =================================================================
# 2. FUNÇÕES DE APOIO (LÓGICA E EXECUÇÃO)
# =================================================================

def determinar_ala(hoje: datetime) -> str:
    """Calcula qual ala está de serviço com base na data e hora."""
    if hoje.time() < dttime(7, 45):
        hoje -= timedelta(days=1)
    
    sequencia = ['4ª', '1ª', '2ª', '3ª']
    data_ref = datetime(2025, 1, 1, 7, 45)
    dias = (hoje.date() - data_ref.date()).days
    return sequencia[dias % len(sequencia)]

def executar_script(script_name: str, background: bool = False):
    """Executa scripts localizados dentro da pasta 'src'."""
    python_exe = sys.executable
    # IMPORTANTE: Agora o código sabe que os scripts estão em /src
    script_path = SRC_DIR / script_name
    
    if not script_path.exists():
        st.error(f"❌ Erro: O script '{script_name}' não foi encontrado em {SRC_DIR}")
        return

    try:
        if background:
            subprocess.Popen(
                [python_exe, str(script_path)],
                cwd=str(ROOT_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
            )
            st.success(f"🚀 {script_name} iniciado em segundo plano.")
        else:
            subprocess.run(
                [python_exe, str(script_path)],
                cwd=str(ROOT_DIR),
                check=True,
                capture_output=True,
                text=True
            )
            st.success(f"✅ {script_name} executado com sucesso!")
    except Exception as e:
        st.error(f"💥 Falha ao executar {script_name}: {e}")

# =================================================================
# 3. INTERFACE (STREAMLIT)
# =================================================================

def mostrar_dados_ocorrencias():

    if not ARQUIVO_OCORRENCIAS.exists():
        st.warning(f"⚠️ Banco de dados não encontrado: {ARQUIVO_OCORRENCIAS.name}")
        return

    try:

        df = pd.read_excel(ARQUIVO_OCORRENCIAS)
        
        if df.empty:
            st.info("📭 O arquivo Excel está vazio.")
            return
        
        coluna_data = 'Data/hora de criação'
        
        if coluna_data in df.columns:

            df[coluna_data] = pd.to_datetime(
                df[coluna_data], 
                dayfirst=True,        
                errors='coerce'        
            )
            
            df = df.dropna(subset=[coluna_data])
            df = df.sort_values(coluna_data, ascending=False)

        st.subheader("📋 Últimas Ocorrências (Excel)")
        st.dataframe(
            df.head(25),
            use_container_width=True
        )

    except Exception as e:
        st.error(f"❌ Erro ao carregar o Excel: {e}")

def main():
    st.set_page_config(page_title="Cad Automation", layout="wide")
    
    with st.sidebar:
        st.title("🛡️ Sistema CAD")
        menu = option_menu(
            menu_title="Menu Principal",
            options=["Automação", "Disparos", "Recursos"],
            icons=["gear", "chat-text", "box"],
            default_index=0,
            styles={"nav-link-selected": {"background-color": "#02ab21"}}
        )

    if menu == "Automação":
        st.header("⚙️ Painel de Controle")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Sincronizar Dados (Completo)"):
                executar_script("main.py")
                executar_script("organize.py")
                st.rerun()
        
        with col2:
            if st.button("🔄 Atualizar Últimos 3 Dias"):
                executar_script("main_ultimos_3_dias.py")
                executar_script("organize.py")
                st.rerun()
        
        st.divider()
        mostrar_dados_ocorrencias()

    elif menu == "Disparos":
        st.header("📲 Gerenciamento de Mensagens")
        st.info(f"Ala atual: **{determinar_ala(datetime.now())}**")
        
        if st.button("🟢 Enviar para WhatsApp"):
            # Aqui você deve colocar o nome real do seu script de whatsapp
            executar_script("organize.py") 
            st.success("Comando enviado!")

if __name__ == "__main__":
    main()