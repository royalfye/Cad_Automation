from pathlib import Path

def gerar_arvore(diretorio, prefixo=""):
    """
    Gera uma representação visual em árvore de um diretório.
    """
    diretorio = Path(diretorio)
    
    # Filtramos o que não queremos mostrar (boas práticas)
    itens_para_ignorar = {'.git', '__pycache__', '.venv', 'venv', '.vscode', '.DS_Store'}
    
    # Pegamos a lista de arquivos e pastas, filtrando os ignorados
    conteudo = [item for item in diretorio.iterdir() if item.name not in itens_para_ignorar]
    
    # Ordenamos para que pastas apareçam primeiro ou por ordem alfabética
    conteudo.sort(key=lambda x: (x.is_file(), x.name.lower()))

    # Quantidade total de itens para saber qual é o último
    total = len(conteudo)

    for i, item in enumerate(conteudo):
        # Verifica se é o último item da lista atual
        e_ultimo = (i == total - 1)
        
        # Define o conector visual
        conector = "└── " if e_ultimo else "├── "
        
        # Exibe o nome (com uma barra se for pasta)
        nome_exibido = f"{item.name}/" if item.is_dir() else item.name
        print(f"{prefixo}{conector}{nome_exibido}")

        # Se for uma pasta, chama a função novamente para listar o que está dentro
        if item.is_dir():
            # Se for o último, o prefixo da próxima linha fica vazio, 
            # senão, adiciona uma linha vertical
            novo_prefixo = prefixo + ("    " if e_ultimo else "│   ")
            gerar_arvore(item, novo_prefixo)

if __name__ == "__main__":
    pasta_raiz = "."  # Pasta atual
    print(f"{Path(pasta_raiz).absolute().name}/") # Imprime o nome da pasta principal
    gerar_arvore(pasta_raiz)