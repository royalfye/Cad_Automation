# cad_verify.py
import time
import pyautogui
import pygetwindow as gw

nome_janela = "CAD - Solução de Controle do Atendimento e Despacho de Emergência Policial e de Bombeiros"
cor_desejada = (0, 153, 0)
regiao = (7, 462, 266, 338)

def maximizar_janela(titulo):
    windows = gw.getWindowsWithTitle(titulo)
    if not windows:
        return False
    janela = windows[0]
    if not janela.isMaximized:
        janela.maximize()
        time.sleep(0.5)
    janela.activate()
    time.sleep(0.5)
    return True

def verificar_cor(cor, regiao):
    img = pyautogui.screenshot(region=regiao)
    px = img.load()
    w, h = img.size
    for x in range(w):
        for y in range(h):
            if px[x, y] == cor:
                return True
    return False

def detecta_nova_ocorrencia() -> bool:
    if not maximizar_janela(nome_janela):
        return False
    return verificar_cor(cor_desejada, regiao)

if __name__ == "__main__":
    if detecta_nova_ocorrencia():
        print("NOVA OCORRÊNCIA")
    else:
        print("Nenhuma nova ocorrência detectada.")
