# automacao.py
import streamlit as st
import os
import sys  
import pandas as pd
import subprocess
from pathlib import Path
from datetime import datetime, time as dttime, timedelta

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EXCEL_PATH = ROOT_DIR / "data" / "chamadas_csv" / "nova_planilha_ocorrencias.xlsx"

def determinar_ala(data_hora_str):
    """
    Determina a ala (4ª, 1ª, 2ª, 3ª) com base na data e hora fornecida como string.
    Considera a transição de plantão às 07:45.
    """
    try:
        data_hora = pd.to_datetime(data_hora_str, format='%d/%m/%Y %H:%M', dayfirst=True, errors='coerce')

        if pd.isna(data_hora):
             return "Inválida"

        data_referencia = pd.to_datetime('01/01/2025 07:45:00', format='%d/%m/%Y %H:%M:%S')
        plantao_inicio_hora = dttime(7, 45) 
        if data_hora.time() < plantao_inicio_hora:
            data_para_calculo = data_hora.date() - timedelta(days=1)
        else:
            data_para_calculo = data_hora.date()

        dias_offset = (data_para_calculo - data_referencia.date()).days
        sequencia_alas = ['4ª', '1ª', '2ª', '3ª']
        indice_ala = dias_offset % len(sequencia_alas) # Use len() para segurança

        return sequencia_alas[indice_ala]
    except Exception as e:
        st.error(f"Erro ao determinar a ala para '{data_hora_str}': {e}")
        return "Erro Cálculo" # Indica erro no cálculo



def executar_script(script_name: str, ROOT_DIR: str):
    python_exe = sys.executable
    script_path = ROOT_DIR / "src" / script_name

    if not os.path.exists(script_path):
        st.error(f"Script não encontrado: {script_path}")
        return
    
    env = {**dict(st.os.environ), 'PYTHONIOENCODING': 'utf-8'}

    try:
        with st.spinner(f"Executando {script_name}..."):
            process = subprocess.run(
                [python_exe, str(script_path)],
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=env
            )
        
        if process.returncode == 0:
            st.success(f"{script_name} finalizado!")
            if process.stdout: st.expander("Ver log").code(process.stdout)
        else:
            st.error(f"Falha em {script_name}")
            st.code(process.stderr)
            
    except Exception as e:
        st.error(f"Erro fatal: {e}")

def carregar_dados_ocorrencias():
    if not EXCEL_PATH.exists():
        return None
    
    df = pd.read_excel(EXCEL_PATH, dtype=str)

    return df

def mostrar_ocorrencias_atual():
    excel_file = EXCEL_PATH
    st.subheader("Ocorrências do Plantão Atual (com Recursos Empenhados)")

    if not os.path.exists(excel_file):
        st.warning(f"Arquivo de ocorrências não encontrado: {excel_file}")
        return

    try:

        df = pd.read_excel(excel_file, dtype=str)

        if df.empty:
            st.info("A planilha de ocorrências está vazia.")
            return

        if 'Data/hora de criação' not in df.columns:
            st.warning("Coluna 'Data/hora de criação' não encontrada na planilha de ocorrências.")
            return 

        df['Data/hora de criação'] = pd.to_datetime(
            df['Data/hora de criação'],
            format='%d/%m/%Y %H:%M',
            dayfirst=True,
            errors='coerce'
        )

        df.dropna(subset=['Data/hora de criação'], inplace=True)

        if df.empty:
            st.info("Nenhuma ocorrência válida encontrada (após limpeza de data).")
            return

        df['ALA'] = df['Data/hora de criação'].dt.strftime('%d/%m/%Y %H:%M').apply(determinar_ala)

        agora = datetime.now()
        ala_atual_agora = determinar_ala(agora.strftime('%d/%m/%Y %H:%M'))

        plantao_inicio_hora_fixa = dttime(7, 45)
        if agora.time() < plantao_inicio_hora_fixa:
            inicio_plantao = datetime.combine((agora - timedelta(days=1)).date(), plantao_inicio_hora_fixa)
        else:
            inicio_plantao = datetime.combine(agora.date(), plantao_inicio_hora_fixa)
        fim_plantao = inicio_plantao + timedelta(hours=24)

        st.write(f"Período do Plantão Atual da **{ala_atual_agora}**: {inicio_plantao.strftime('%d/%m %H:%M')} - {fim_plantao.strftime('%d/%m %H:%M')}")

        mask = (
            (df['Data/hora de criação'] >= inicio_plantao) &
            (df['Data/hora de criação'] < fim_plantao) &
            (df['ALA'] == ala_atual_agora)
        )
        if 'Recursos empenhados' in df.columns:
            mask = mask & (df['Recursos empenhados'].astype(str).str.strip() != '')
        else:
             st.warning("Coluna 'Recursos empenhados' não encontrada. Exibindo todas as ocorrências da ALA e Plantão.")

        df_plantao_filtrado = df.loc[mask].copy()

        if df_plantao_filtrado.empty:
            st.info(f"Não há ocorrências (com recursos empenhados, se a coluna existir) para a {ala_atual_agora} neste plantão.")
        else:
            st.write(f"Total de ocorrências encontradas: {len(df_plantao_filtrado)}")
            if 'Classe' in df_plantao_filtrado.columns and not df_plantao_filtrado['Classe'].dropna().empty:
                st.write("Contagem por Classe:")
                contagem_classe = df_plantao_filtrado['Classe'].value_counts()
                for classe, qt in contagem_classe.items():
                     st.write(f"- **{classe}**: {qt}")
            else:
                 st.info("Coluna 'Classe' não encontrada ou vazia para contagem.")

    except FileNotFoundError:
        st.warning(f"Arquivo de ocorrências não encontrado: {excel_file}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar as ocorrências do plantão atual: {e}")


def mostrar_ultimas_ocorrencias():
    excel_file = EXCEL_PATH
    st.subheader("Últimas 25 Ocorrências Registradas (Arquivo Completo)")

    if not os.path.exists(excel_file):
        st.warning(f"Arquivo de ocorrências não encontrado: {excel_file}")
        return

    try:
        df = pd.read_excel(excel_file, dtype=str)

        if df.empty:
            st.info("O arquivo de ocorrências está vazio.")
            return

        if 'Data/hora de criação' in df.columns:
            df['Data/hora de criação'] = pd.to_datetime(
                df['Data/hora de criação'], format='%d/%m/%Y %H:%M', dayfirst=True, errors='coerce'
            )
            df.dropna(subset=['Data/hora de criação'], inplace=True) # Remove linhas com data/hora inválida
        else:
            st.warning("Coluna 'Data/hora de criação' não encontrada para ordenar. Exibindo últimas 25 linhas em ordem original.")
            ultimas = df.tail(25).copy() # Use .copy()
            if 'ALA' not in ultimas.columns:
                 ultimas['ALA'] = "Sem Data Col"

            cols_to_show_base = ['Data/hora de criação', 'Classe', 'Tipo/Subtipo', 'Situação', 'Endereço', 'Recursos empenhados', 'ALA']
            cols_to_show_existing = [col for col in cols_to_show_base if col in ultimas.columns]
            st.dataframe(ultimas[cols_to_show_existing if cols_to_show_existing else ultimas.columns]) 
            return

        if df.empty:
            st.info("Nenhuma ocorrência válida encontrada para exibir (após limpeza de data).")
            return

        ultimas = df.sort_values('Data/hora de criação', ascending=False).head(25).copy()
        ultimas['ALA'] = ultimas['Data/hora de criação'].dt.strftime('%d/%m/%Y %H:%M').apply(determinar_ala)
        cols_to_show_base = ['Data/hora de criação', 'Classe', 'Tipo/Subtipo', 'Situação', 'Endereço', 'Recursos empenhados', 'ALA']

        cols_to_show_existing = [col for col in cols_to_show_base if col in ultimas.columns]

        if not cols_to_show_existing:
             st.warning("Nenhuma das colunas esperadas encontrada no DataFrame das últimas ocorrências.")
             st.dataframe(ultimas) 
        else:
             st.dataframe(ultimas[cols_to_show_existing]) 

    except FileNotFoundError:

        st.warning(f"Arquivo de ocorrências não encontrado: {excel_file}")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar as últimas ocorrências: {e}")



def aba_automacao():
    st.header("Painel de Automação")
    st.write("Aqui você pode executar as automações de coleta e organização de dados.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Executar Coleta e Organização", help="Roda os scripts main.py e organize.py"):
            st.info("Iniciando execução da Coleta e Organização...")
            executar_script("main.py", ROOT_DIR)
            executar_script("organize.py", ROOT_DIR)
            st.success("Coleta e Organização concluídas (ver logs acima para detalhes).")
            st.warning("Recarregando a página para atualizar os dados exibidos...")

    with col2:
        st.button("⏹️ Parar Automação (não funcional)", disabled=True, help="Funcionalidade a ser implementada (requer lógica de controle de processo avançada).")

    with col3:

        if st.button("🔄 Atualizar Últimos 3 Dias", help="Executa main_ultimos_3_dias.py e organize.py (se os scripts existirem)."):
            st.info("Iniciando execução da Atualização dos Últimos 3 Dias...")
            script_ultimos_3_dias_path = os.path.join(ROOT_DIR, "main_ultimos_3_dias.py")
            if os.path.exists(script_ultimos_3_dias_path):
                executar_script("main_ultimos_3_dias.py", ROOT_DIR)
                executar_script("organize.py", ROOT_DIR)
                st.success("Atualização dos Últimos 3 Dias concluída (ver logs acima para detalhes).")
                st.warning("Recarregando a página para atualizar os dados exibidos...")

            else:
                 st.error(f"Script 'main_ultimos_3_dias.py' não encontrado em {ROOT_DIR}. Não foi possível executar a atualização.")

    st.markdown("---") 
    st.info("Clique no botão abaixo para carregar os dados mais recentes da planilha.")
    if st.button("Atualizar Visualização de Dados"):
        st.rerun() 

    st.markdown("---") 

    mostrar_ocorrencias_atual()
    st.markdown("---")
    mostrar_ultimas_ocorrencias()

