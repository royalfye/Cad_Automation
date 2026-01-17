import pygetwindow as gw
import pyautogui
import pytesseract
import time
import os

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Ajuste o caminho do Tesseract conforme sua instalação
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- CONFIGURAÇÃO DE CAMINHOS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
DATA_RAW_DIR = os.path.join(ROOT_DIR, 'data', 'raw')

# Mapeamento de Recursos
IMG_CABECALHO = os.path.join(ASSETS_DIR, 'cabecalho.png')
IMG_LAPIS = os.path.join(ASSETS_DIR, 'lapis.png')
IMGS_HISTORICO = [
    os.path.join(ASSETS_DIR, 'historicos.png'),
    os.path.join(ASSETS_DIR, 'historicos_2.png')
]
IMGS_DADOS_GERAIS = [
    os.path.join(ASSETS_DIR, 'dados_gerais.png'),
    os.path.join(ASSETS_DIR, 'dados_gerais2.png')
]

# Garantir que a pasta de dados existe
os.makedirs(DATA_RAW_DIR, exist_ok=True)

def clicar_na_imagem(caminhos_imagem, nome_log, confidence=0.8, duplo_clique=False):
    if isinstance(caminhos_imagem, str):
        caminhos_imagem = [caminhos_imagem]
    
    for caminho in caminhos_imagem:
        try:
            if not os.path.exists(caminho): continue
            posicao = pyautogui.locateOnScreen(caminho, confidence=confidence)
            if posicao:
                centro = pyautogui.center(posicao)
                if duplo_clique: pyautogui.doubleClick(centro)
                else: pyautogui.click(centro)
                print(f"Sucesso: {nome_log} clicado.")
                return True
        except Exception as e:
            print(f"Erro ao processar {nome_log}: {e}")
    return False

def extrair_texto_ocr():
    """Realiza a captura da região definida e extrai o texto."""
    print("Iniciando extração de texto...")
    try:
        # Suas coordenadas validadas
        regiao = (337, 345, 477, 214)
        
        # Captura e Debug
        screenshot = pyautogui.screenshot(region=regiao)
        screenshot.save(os.path.join(DATA_RAW_DIR, 'ultima_extracao.png'))
        
        # Melhora imagem e processa OCR
        largura, altura = screenshot.size
        screenshot = screenshot.resize((largura * 2, altura * 2))
        texto = pytesseract.image_to_string(screenshot, lang='por', config='--psm 6')
        
        return texto.strip()
    except Exception as e:
        print(f"Falha no OCR: {e}")
        return None

def executar_automacao():
    TITULO_CAD = "CAD - Solução de Controle do Atendimento e Despacho de Emergência Policial e de Bombeiros"
    
    # 1. Focar Janela
    janelas = gw.getWindowsWithTitle(TITULO_CAD)
    if not janelas:
        print("CAD não encontrado.")
        return
    
    cad = janelas[0]
    cad.activate()
    if cad.isMinimized: cad.restore()
    cad.maximize()
    time.sleep(1)

    # 2. Abrir Chamada (Lógica do cabeçalho)
    ponto_cab = pyautogui.locateOnScreen(IMG_CABECALHO, confidence=0.8)
    if ponto_cab:
        cx, cy = pyautogui.center(ponto_cab)
        pyautogui.doubleClick(cx, cy + 30)
        time.sleep(2) # Espera carregar detalhes

        # 3. Navegar para Históricos
        if clicar_na_imagem(IMGS_HISTORICO, "Aba Históricos"):
            time.sleep(1)

            # 4. Abrir Detalhes (Lápis)
            if clicar_na_imagem(IMG_LAPIS, "Ícone Lápis"):
                time.sleep(1.5) # Tempo para o texto carregar na janelinha
                
                # 5. EXTRAÇÃO FINAL
                texto_extraido = extrair_texto_ocr()
                
                if texto_extraido is not None:
                    print("Finalizando extração e limpando a tela...")
                    
                    # A. Fechar a janela do Lápis
                    pyautogui.hotkey('alt', 'f4') 
                    time.sleep(1) # Pequena pausa para a janela fechar
                    
                    # B. Voltar para a aba 'Dados Gerais'
                    # Usamos a nossa função clicar_na_imagem que já lida com os dois estados (normal/azul)
                    clicar_na_imagem(IMGS_DADOS_GERAIS, "Aba Dados Gerais")
                    
                    print("Sistema pronto para a próxima ocorrência.")
                    return texto_extraido
                else:
                    print("Texto não capturado.")
    
    return None

if __name__ == "__main__":
    executar_automacao()