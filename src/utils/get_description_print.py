import pytesseract
import pyautogui
import os
import time

# --- CONFIGURAÇÃO ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Lógica para salvar o print na pasta data/raw
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
DEBUG_PATH = os.path.join(ROOT_DIR, 'data', 'raw', 'debug_cad.png')

def extrair_dados_cad():
    print("Iniciando processo de captura...")
    try:
        # 1. Definição da Região (suas coordenadas)
        regiao = (337, 345, 477, 214)
        
        # 2. Tira o print
        screenshot = pyautogui.screenshot(region=regiao)
        
        # 3. SALVA O PRINT (Essencial para você conferir se está certo)
        # Cria a pasta se não existir
        os.makedirs(os.path.dirname(DEBUG_PATH), exist_ok=True)
        screenshot.save(DEBUG_PATH)
        print(f"Print da região salvo em: {DEBUG_PATH}")
        
        # 4. Melhora a imagem para o OCR
        largura, altura = screenshot.size
        screenshot = screenshot.resize((largura * 2, altura * 2))
        
        # 5. Executa o OCR
        config_ocr = '--psm 6'
        texto_puro = pytesseract.image_to_string(screenshot, lang='por', config=config_ocr)
        
        texto_limpo = texto_puro.strip()
        
        if texto_limpo:
            print("\n=== TEXTO EXTRAÍDO ===")
            print(texto_limpo)
            print("======================\n")
            return texto_limpo
        else:
            print("Aviso: O OCR foi executado, mas a imagem parece não conter texto legível.")
            return None

    except Exception as e:
        print(f"Erro na extração OCR: {e}")
        return None

# --- O QUE ESTAVA FALTANDO: A CHAMADA DO CÓDIGO ---
if __name__ == "__main__":
    # Dá 2 segundos para você clicar na janela do CAD se necessário
    print("O script iniciará em 2 segundos... Prepare a tela do CAD.")
    time.sleep(2)
    
    resultado = extrair_dados_cad()
    
    if not resultado:
        print("Dica: Abra o arquivo 'data/raw/debug_cad.png' e veja se o texto aparece lá.")