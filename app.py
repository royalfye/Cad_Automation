import streamlit as st
import pandas as pd
from pathlib import Path
from typing import Optional
from streamlit_option_menu import option_menu
from src.main import run_full_automation

ROOT_DIR = Path(__file__).resolve().parent
ARQUIVO_OCORRENCIAS = ROOT_DIR / "data" / "chamadas_csv" / "nova_planilha_ocorrencias.xlsx"

@st.cache_data(ttl=300)
def carregar_dados(caminho: Path) -> Optional[pd.DataFrame]:
    if not caminho.exists():
        return None
    
    try:
        df = pd.read_excel(caminho)
        
        df['Data/hora de criação'] = pd.to_datetime(
            df['Data/hora de criação'], 
            format="%d/%m/%Y %H:%M", 
            dayfirst=True,
            errors='coerce'
        )
        
        return df.sort_values(by='Data/hora de criação', ascending=False).reset_index(drop=True)
        
    except Exception as e:
        st.error(f"Erro crítico ao ler Excel: {e}")
        return None

def formatar_uma_ocorrencia(row: pd.Series) -> str:
    data_formatada = row['Data/hora de criação'].strftime('%d/%m/%Y %H:%M')
    
    # Verificamos se a coluna 'Histórico' existe e se tem conteúdo
    # O .get() evita que o código quebre caso a coluna ainda não exista no Excel
    historico = row.get('Histórico', "(Aguardando preenchimento)")
    
    # Se o valor for nulo (vazio no Excel), colocamos o aviso
    if pd.isna(historico) or str(historico).strip() == "":
        historico = "(Aguardando preenchimento)"

    return (
        f"🚨 *NOVA OCORRÊNCIA*\n\n"
        f"📅 *Data/Hora:* {data_formatada}\n"
        f"📝 *Natureza:* {row['Natureza']}\n"
        f"📍 *Endereço:* {row['Local do fato']}\n"
        f"📖 *Histórico:* {historico}"
    )

def formatar_apenas_historico(row: pd.Series) -> str:
    """Formata apenas o histórico com o ID da chamada para referência."""
    historico = row.get('Histórico', "")
    if pd.isna(historico) or str(historico).strip() == "":
        return "⚠️ *Aviso:* Histórico ainda não preenchido para esta chamada."
    
    return (
        f"📖 *ATUALIZAÇÃO DE HISTÓRICO*\n"
        f"Nº Chamada: `{row['Nº chamada']}`\n\n"
        f"{historico}"
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

    elif menu == "Disparos":
        st.header("📲 Central de Disparos")
        
        if df is not None and not df.empty:
            # --- MELHORIA AQUI: Formatação inteligente ---
            # Criamos uma função interna para formatar o nome que aparece no selectbox
            def formatar_label(idx):
                row = df.loc[idx]
                data = row['Data/hora de criação'].strftime('%d/%m/%Y %H:%M')
                return f"{data} - {row['Natureza']} (ID: {row['Nº chamada']})"

            # O selectbox armazena o ÍNDICE original do DataFrame, 
            # mas mostra ao usuário o texto bonito da função acima
            indice_escolhido = st.selectbox(
                "Selecione a ocorrência para despacho:",
                options=df.index,
                format_func=formatar_label
            )
            
            # Recuperamos a linha selecionada diretamente pelo índice original
            row = df.loc[indice_escolhido]
            id_chamada = row['Nº chamada']
            
            st.divider()

            # --- Layout de Trabalho ---
            col_info, col_copy = st.columns([1, 1])
            
            with col_info:
                st.subheader("📍 Detalhes")
                # Uso de f-string limpa e organizada
                st.markdown(f"""
                **Nº Chamada:** `{id_chamada}`  
                **Natureza:** {row['Natureza']}  
                **Local:** {row['Local do fato']}  
                **Unidade:** {row['Unidade Responsável']}
                """)
            
            with col_copy:
                st.subheader("✍️ Formatação para Envio")
                tab_completa, tab_historico = st.tabs(["📋 Chamada Completa", "📖 Só Histórico"])
                
                with tab_completa:
                    texto_pronto = formatar_uma_ocorrencia(row)
                    # O st.code cria o botão de 'copiar' automaticamente
                    st.code(texto_pronto, language="text") 
                    
                    with st.expander("📝 Editar texto antes de enviar"):
                        st.text_area("Edição:", value=texto_pronto, height=150, key=f"edit_full_{id_chamada}")

                with tab_historico:
                    so_historico = formatar_apenas_historico(row)
                    # Aqui está o seu 'botão' de copiar para o histórico
                    st.code(so_historico, language="text")
                    
                    with st.expander("📝 Editar histórico antes de enviar"):
                        st.text_area("Edição:", value=so_historico, height=150, key=f"edit_hist_{id_chamada}")

                with tab_historico:
                    so_historico = formatar_apenas_historico(row)
                    st.text_area(
                        "Apenas o Histórico:", 
                        value=so_historico, 
                        height=200,
                        key=f"hist_{id_chamada}" 
                    )
                    if st.button("📢 Enviar Atualização", key=f"btn_hist_{id_chamada}"):
                        st.success("Atualização enviada!")
        else:
            st.warning("Sem dados disponíveis para disparos. Vá em Automação e sincronize.")

if __name__ == "__main__":
    main()