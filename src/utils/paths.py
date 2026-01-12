from pathlib import Path

# 1. Define a Raiz do Projeto (Cad_Automation/)
# Como este arquivo está em src/utils/, precisamos subir 2 níveis para chegar na raiz
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 2. Define os Caminhos das Pastas Principais
ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data"
SRC_DIR = ROOT_DIR / "src"

# 3. Subpastas de Dados (Organização Profissional)
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CHAMADAS_DIR = DATA_DIR / "chamadas_csv"

# 4. Verificação de Integridade (Opcional, mas recomendado para automação)
def check_directories():
    """Garante que as pastas essenciais existam antes de iniciar a automação."""
    for folder in [ASSETS_DIR, DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, CHAMADAS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Teste isolado para validar os caminhos
    print(f"--- VALIDANDO ESTRUTURA ---")
    print(f"Raiz: {ROOT_DIR}")
    print(f"Assets: {ASSETS_DIR.exists()}")
    print(f"Dados: {DATA_DIR.exists()}")