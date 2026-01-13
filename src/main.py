import time
import pyautogui
import pandas as pd
import pygetwindow as gw
import logging
import subprocess
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from src.organize import organizar_planilha

# Configurações de logs e segurança
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
pyautogui.FAILSAFE = True

# --- RECOLOQUE AQUI SUAS FUNÇÕES ORIGINAIS DE TRATAMENTO ---

def determinar_ala(data_hora_str):
    try:
        data_hora = pd.to_datetime(data_hora_str, format='%d/%m/%Y %H:%M', errors='raise')
        data_referencia = pd.to_datetime('01/01/2025 07:45:00')
        if data_hora.time() < pd.to_datetime('07:45:00').time():
            dias_offset = (data_hora.date() - data_referencia.date()).days - 1
        else:
            dias_offset = (data_hora.date() - data_referencia.date()).days
        sequencia_alas = ['4ª', '1ª', '2ª', '3ª']
        return sequencia_alas[dias_offset % 4]
    except:
        return "Indefinida"

def atualizar_dados_occurrences(csv_file_path, excel_file_path):
    """Sua lógica original de Merge e Filtro"""
    if not csv_file_path.exists():
        logging.error("CSV não encontrado.")
        return
    
    try:
        df_novo = pd.read_csv(csv_file_path, encoding='latin1', sep=';', dtype=str)
        df_novo.columns = df_novo.columns.str.strip()
        
        colunas_necessarias = [
            'Data/hora de criação', 'Data/hora da situação atual', 'Nº chamada', 'Natureza',
            'Local do fato', 'Unidade Responsável', 'Recursos empenhados'
        ]
        
        df_novo = df_novo[df_novo['Unidade Responsável'].str.contains(r'\(PASSOS\)', na=False)]
        df_novo_filtrado = df_novo[colunas_necessarias].copy()
        
        # Limpeza e ALA
        df_novo_filtrado['Natureza'] = df_novo_filtrado['Natureza'].str.replace(r'\s*\(.*$', '', regex=True)
        df_novo_filtrado['Classe'] = df_novo_filtrado['Natureza'].str.strip().str[0]
        df_novo_filtrado['ALA'] = df_novo_filtrado['Data/hora de criação'].apply(determinar_ala)
        
        df_novo_filtrado.rename(columns={'Data/hora da situação atual': 'Data/hora final'}, inplace=True)
        
        if excel_file_path.exists():
            df_existente = pd.read_excel(excel_file_path, dtype=str)
            df_final = pd.concat([df_existente, df_novo_filtrado]).drop_duplicates(subset=['Nº chamada'], keep='last')
            df_final.to_excel(excel_file_path, index=False)
        else:
            df_novo_filtrado.to_excel(excel_file_path, index=False)
            
    except Exception as e:
        logging.error(f"Erro no tratamento: {e}")

# --- FUNÇÃO DE AUTOMAÇÃO (A QUE VOCÊ JÁ TINHA) ---

def activate_window(window_title):
    """Sua função de sempre, com o reforço para o Streamlit"""
    while True:
        try:
            win = gw.getWindowsWithTitle(window_title)[0]
            if win.isMinimized:
                win.restore()
            win.activate()
            win.maximize()
            logging.info(f"Janela ativada: {window_title}")
            break
        except IndexError:
            logging.warning(f"Esperando pela janela: {window_title}")
            time.sleep(1)
        except Exception:
            # Se der o 'Erro 0', ele ignora e tenta de novo no próximo ciclo do while
            time.sleep(1)

def run_full_automation():
    BASE_DIR = Path(__file__).resolve().parent.parent
    ASSETS = BASE_DIR / "assets"
    CSV_PATH = BASE_DIR / "data" / "chamadas_csv" / "ocorrencias.csv"
    EXCEL_PATH = BASE_DIR / "data" / "chamadas_csv" / "nova_planilha_ocorrencias.xlsx"
    window_title = "CAD - Solução de Controle do Atendimento e Despacho de Emergência Policial e de Bombeiros"

    # 1. Fecha o Excel
    subprocess.run(["taskkill", "/im", "EXCEL.EXE", "/f"], capture_output=True)
    
    # 2. Ativa Janela
    window_title = "CAD - Solução de Controle do Atendimento e Despacho de Emergência Policial e de Bombeiros"
    activate_window(window_title)
    
    time.sleep(1)

    # 3. Cliques (Respeitando sua sequência original)
    try:
        pyautogui.click(str(ASSETS / 'chamadas_button.png'))
        time.sleep(1)
        pyautogui.click(str(ASSETS / 'pesquisa_button.png'))
        time.sleep(1)
        
        # Coordenada fixa que você usava
        pyautogui.click(x=339, y=207)
        time.sleep(1)
        
        # Busca Passos
        seta = str(ASSETS / 'seta_button.png')
        if pyautogui.locateOnScreen(seta, confidence=0.7):
            pyautogui.click(seta)
            pyautogui.write("PASSOS")
            time.sleep(1)
            
            ponto = pyautogui.locateCenterOnScreen(str(ASSETS / 'passos_exibido.png'), confidence=0.7)
            if ponto: pyautogui.click(ponto)

        # Exportação
        pyautogui.click(x=1153, y=414) # Pesquisar
        time.sleep(4)
        pyautogui.press('f12')
        time.sleep(1)
        pyautogui.write(str(CSV_PATH.absolute()))
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('alt', 'f4')

        try:
            pesquisa_window = gw.getWindowsWithTitle("Pesquisa Chamadas")[0]
            pesquisa_window.activate()
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
        except IndexError:
            logging.warning("Janela 'Pesquisa Chamadas' não encontrada.")

        try:
            ocorrencias_csv_window = gw.getWindowsWithTitle("ocorrencias.csv - Excel")[0]
            ocorrencias_csv_window.activate()
            time.sleep(1)
            pyautogui.hotkey('alt', 'f4')
        except IndexError:
            logging.warning("Janela 'ocorrencias.csv - Excel' não encontrada.")
        
        # 4. Tratamento dos Dados (Sua lógica de volta!)
        atualizar_dados_occurrences(CSV_PATH, EXCEL_PATH)
        
        # 5. Formatação Visual (Chama o organize.py)
        from src.organize import organizar_planilha
        organizar_planilha(EXCEL_PATH)
        
        return True
    except Exception as e:
        logging.error(f"Erro: {e}")
        return False

if __name__ == "__main__":
    run_full_automation()