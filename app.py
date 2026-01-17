import streamlit as st
import pandas as pd
from pathlib import Path
from src.main import run_full_automation

ROOT_DIR = Path(__file__).resolve().parent
ARQUIVO_OCORRENCIAS = ROOT_DIR / "data" / "chamadas_csv" / "nova_planilha_ocorrencias.xlsx"

@st.cache_data(ttl=300)
@st.cache_data(ttl=300)
def carregar_dados(caminho: Path):
    if not caminho.exists():
        return None
    try:
        df = pd.read_excel(caminho)
        
        df['Data/hora de criação'] = pd.to_datetime(
            df['Data/hora de criação'], 
            format="%d/%m/%Y %H:%M", 
            dayfirst=True
        )
        
        # 2. Ordenação Garantida (Mais recentes no topo)
        df = df.sort_values(by='Data/hora de criação', ascending=False)
        
        return df.reset_index(drop=True)
        
    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        return None

def formatar_uma_ocorrencia(row):
    return (
        f"🚨 *NOVA OCORRÊNCIA*\n\n"
        f"📅 *Data/Hora:* {row['Data/hora de criação']}\n"
        f"📝 *Natureza:* {row['Natureza']}\n"
        f"📍 *Endereço:* {row['Local do fato']}\n"
        f"📖 *Histórico:* (Aguardando preenchimento)"
    )

def main():
    st.set_page_config(page_title="Cad Automation", layout="wide", page_icon="🛡️")

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ Sistema CAD")
        from streamlit_option_menu import option_menu
        menu = option_menu(
            "Menu Principal", ["Automação", "Disparos"],
            icons=["gear", "chat-text"], default_index=0
        )

    # Carregamento global dos dados
    df = carregar_dados(ARQUIVO_OCORRENCIAS)

    # --- ABA: AUTOMAÇÃO ---
    if menu == "Automação":
        st.header("⚙️ Painel de Controle")
        if st.button("▶️ Sincronizar e Organizar", use_container_width=True):
            with st.spinner("Robô em ação..."):
                if run_full_automation():
                    st.success("Dados sincronizados!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("Falha na automação.")

        st.divider()
        st.subheader("📋 Planilha Completa (Recentes primeiro)")
        if df is not None:
            st.dataframe(df, use_container_width=True, height=400)
        else:
            st.info("Nenhum dado encontrado.")

    # --- ABA: DISPAROS (Aqui é onde a mágica acontece) ---
    # --- ABA: DISPAROS ---
    elif menu == "Disparos":
        st.header("📲 Central de Disparos")
        
        if df is not None and not df.empty:
            # 1. Seleção da Ocorrência
            # Criamos uma lista formatada: "16/01/2026 18:51 - NATUREZA"
            opcoes = df.apply(
                lambda x: f"{x['Data/hora de criação'].strftime('%d/%m/%Y %H:%M')} - {x['Natureza']}", 
                axis=1
            ).tolist()
            
            escolha = st.selectbox("Selecione a ocorrência para despacho:", opcoes)
            
            # 2. Filtro da linha selecionada
            # Como o selectbox agora não tem o Nº da chamada fixo no início, 
            # a melhor forma de recuperar a linha é pelo índice da seleção.
            
            # Buscamos o índice da opção escolhida para pegar a linha correspondente no DF
            indice_selecionado = opcoes.index(escolha)
            row = df.iloc[indice_selecionado]
            
            id_chamada = row['Nº chamada'] # Recuperamos o ID original para o histórico
            
            st.divider()

            # 3. Layout de Trabalho
            col_info, col_copy = st.columns([1, 1])
            
            with col_info:
                st.subheader("📍 Detalhes")
                st.markdown(f"""
                **Nº Chamada:** `{id_chamada}`  
                **Natureza:** {row['Natureza']}  
                **Local:** {row['Local do fato']}  
                **Unidade:** {row['Unidade Responsável']}
                """)
            
            with col_copy:
                st.subheader("✍️ Formatação")
                texto_pronto = formatar_uma_ocorrencia(row)
                texto_editavel = st.text_area("Edite o histórico se necessário:", value=texto_pronto, height=200)
                
                # Botão de cópia rápido
                st.code(texto_editavel, language="text")
                
                if st.button("🚀 Confirmar Envio", use_container_width=True):
                    st.balloons()
                    st.success(f"Ocorrência {id_chamada} processada!")
        else:
            st.warning("Sem dados disponíveis para disparos. Vá em Automação e sincronize.")

if __name__ == "__main__":
    main()