# import pyautogui

# # Define as coordenadas da região: (left, top, width, height)
# regiao = (200, 200, 100, 100)

# # Passo 1: Captura a região da tela
# imagem = pyautogui.screenshot(region=regiao)

# # Passo 2: Analisa os pixels
# pixels = imagem.load()

# # Passo 3: Verifica se há algum pixel com a cor RGB desejada
# cor_desejada = (0, 153, 0)
# encontrado = False

# for x in range(regiao[2]):
#     for y in range(regiao[3]):
#         if pixels[x, y] == cor_desejada:
#             encontrado = True
#             print(f"Cor encontrada na posição ({x}, {y}) da região.")
#             break
#     if encontrado:
#         break

# if not encontrado:
#     print("A cor desejada NÃO foi encontrada na região.")


import pyautogui
import time

print("Posicione o mouse na esquina superior esquerda da região e aguarde...")
time.sleep(3)  # Tempo para posicionar o cursor

# Captura a posição
x1, y1 = pyautogui.position()
print(f"Coordenada superior esquerda: ({x1}, {y1})")

print("Posicione o mouse na esquina inferior direita da região e aguarde...")
time.sleep(3)
x2, y2 = pyautogui.position()
print(f"Coordenada inferior direita: ({x2}, {y2})")

# Calcula largura e altura
width = x2 - x1
height = y2 - y1
print(f"Largura: {width}, Altura: {height}")
