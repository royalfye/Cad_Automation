from pynput import mouse
import pyautogui
import time

# def on_click(x, y, button, pressed):
#     if pressed:
#         print(f"Mouse clicado em x={x}, y={y}")

# with mouse.Listener(on_click=on_click) as listener:
#     listener.join()

# def on_click(x, y, button, pressed):
#     if pressed:
#         # Quando o botão for pressionado, captura a cor do pixel na posição do clique
#         color = pyautogui.pixel(x, y)
#         print(f"Clique detectado em ({x}, {y})")
#         print(f"A cor do pixel nesse ponto é: RGB {color}")

# # Cria um ouvinte que monitora os eventos do mouse
# with mouse.Listener(on_click=on_click) as listener:
#     print("Clique com o mouse para capturar a cor do pixel. Para sair, pressione Ctrl+C.")
#     listener.join()

import pygetwindow as gw

# Nome exato da janela
nome_janela = "CAD - Solução de Controle do Atendimento e Despacho de Emergência Policial e de Bombeiros"

# Encontra a janela
windows = gw.getWindowsWithTitle(nome_janela)
if not windows:
    print("Janela não encontrada.")
    exit()

janela = windows[0]

# Ativa a janela
janela.activate()

# Dá um pequeno tempo para a janela ativar
time.sleep(0.5)

# Define as coordenadas da região
regiao = (7, 462, 266, 338)

# Captura a região
imagem = pyautogui.screenshot(region=regiao)

# Analisa os pixels
pixels = imagem.load()

# Cor desejada
cor_desejada = (0, 153, 0)
encontrado = False

for x in range(regiao[2]):
    for y in range(regiao[3]):
        if pixels[x, y] == cor_desejada:
            encontrado = True
            print(f"Cor encontrada na posição ({x}, {y}) da região.")
            break
    if encontrado:
        break

if not encontrado:
    print("A cor desejada NÃO foi encontrada na região.")
