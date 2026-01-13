
---

# 🛡️ CAD Automation & Info Portal

Sistema de automação para extração, tratamento e visualização de dados do sistema **CAD**. O projeto automatiza a exportação de ocorrências policiais/bombeiros e consolida as informações em um painel interativo.

Sua estrutura em árvore está da seguinte forma:

```
Cad_Automation/
├── assets/
│   ├── chamadas_button.png
│   ├── exportar_csv.png
│   ├── passos_exibido.png
│   ├── pesquisa_button.png
│   ├── seta_button.png
│   ├── ultimas_24.png
│   └── ultimos_3.png
├── data/
│   ├── chamadas_csv/
│   │   ├── nova_planilha_ocorrencias.xlsx
│   │   ├── ocorrencias.csv
│   │   └── ocorrencias_classificadas.csv
│   ├── processed/
│   └── raw/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── automacao.py
│   │   ├── disparos.py
│   │   ├── estatisticas.py
│   │   ├── legislacao.py
│   │   ├── recursos.py
│   │   └── telefones.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── def_region.py
│   │   ├── get_window.py
│   │   ├── organizer_tree.py
│   │   ├── paths.py
│   │   └── script_mouse.py
│   ├── __init__.py
│   ├── atualizar_dados_mes.py
│   ├── cad_verify.py
│   ├── main.py
│   ├── main_ultimos_3_dias.py
│   └── organize.py
├── .gitignore
├── app.py
├── Automacao CAD.bat
├── README.md
└── requirements.txt

```

## 🚀 Funcionalidades

* **Extração Robótica:** Utiliza visão computacional e automação de interface (PyAutoGUI) para navegar no sistema CAD e exportar dados.
* **Processamento de Dados:** Filtra ocorrências por unidade (Passos), classifica naturezas e identifica automaticamente a Ala de serviço (1ª a 4ª).
* **Interface Intuitiva:** Exibe os dados consolidados em um dashboard moderno via Streamlit.
* **Organização Excel:** Formata planilhas automaticamente com cores dinâmicas por Ala, bordas e ajuste de colunas.

## 📁 Principais Arquivos e Funções

| Arquivo | Função Principal |
| --- | --- |
| **`app.py`** | **Ponto de entrada.** Gerencia a interface do usuário no navegador e orquestra as chamadas das automações. |
| **`src/main.py`** | **Cérebro da Automação.** Contém a lógica de controle do mouse/teclado para extração no CAD e o merge dos dados novos com os antigos. |
| **`src/organize.py`** | **Estética e Estrutura.** Aplica toda a formatação visual no Excel (cores das alas, bordas e ordenação por data). |
| **`assets/`** | Armazena as imagens de referência para que o robô reconheça botões e ícones na tela. |
| **`data/`** | Local onde o banco de dados (CSV/Excel) é armazenado e atualizado. |

## 🛠️ Como rodar

1. Certifique-se de que o sistema CAD está aberto.
2. Inicie o portal:
```bash
streamlit run app.py

```


3. Clique em **"Sincronizar e Organizar"** e não utilize o mouse até que a janela do CAD seja fechada.


---
