import pygetwindow as gw

# Obter todas as janelas
windows = gw.getAllTitles()

# Filtrar somente janelas com títulos (descartando janelas minimizadas ou sem título)
windows = [w for w in windows if w]

# Mostrar nomes de janelas abertas
for window in windows:
    print(window)
