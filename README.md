## 📝 Descrição Geral

O **Cad_Automation** é um ecossistema de automação (RPA) e visualização de dados desenvolvido para otimizar o fluxo de informações de ocorrências policiais e de bombeiros. O projeto extrai dados brutos de um sistema legado (CAD), processa essas informações, enriquece-as com inteligência visual (OCR) e as disponibiliza em uma interface amigável para despacho via WhatsApp.

## 🛠️ Arquitetura do Sistema

O projeto é dividido em três pilares principais:

### 1. Motor de Automação e Extração (`src/main.py` & `src/get_description.py`)

* **Foco e Navegação:** Utiliza `PyGetWindow` e `PyAutoGUI` para manipular a interface do sistema CAD, realizar pesquisas filtradas por unidade (Ex: PASSOS) e exportar relatórios em `.csv`.
* **Visão Computacional (OCR):** Através do `Pytesseract`, o sistema realiza a leitura de campos de texto não selecionáveis dentro do CAD. Ele captura uma região específica da tela (ROI), processa a imagem para melhorar a nitidez e converte o histórico da ocorrência em texto digital.

### 2. Processamento e Organização (`src/organize.py` & `src/utils/`)

* **Tratamento de Dados:** Utiliza `Pandas` para realizar o merge entre novos dados e o histórico existente, eliminando duplicatas e calculando informações automáticas (como a escala de trabalho/ALA).
* **Estética de Dados:** Utiliza `Openpyxl` para formatar a planilha Excel final, aplicando cores condicionais por ALA e configurando quebras de texto automáticas para o campo de Histórico.

### 3. Interface de Operação (`app.py`)

* **Dashboard Streamlit:** Uma interface web local que permite ao operador disparar a automação com um clique e visualizar a planilha completa.
* **Central de Disparos:** Permite selecionar ocorrências específicas e gera automaticamente dois tipos de formatos para WhatsApp:
* **Chamada Completa:** Dados de localização, natureza e histórico.
* **Atualização de Histórico:** Apenas as novas informações vinculadas ao ID da chamada.



## 📂 Estrutura de Pastas

```text
Cad_Automation/
├── assets/
│   ├── cabecalho.png
│   ├── chamadas_button.png
│   ├── dados_gerais.png
│   ├── dados_gerais2.png
│   ├── exportar_csv.png
│   ├── historicos.png
│   ├── historicos2.png
│   ├── lapis.png
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
│       └── ultima_extracao.png
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── automacao.py
│   │   ├── disparos.py
│   │   ├── estatisticas.py
│   │   ├── legislacao.py
│   │   ├── recursos.py
│   │   └── telefones.py
│   ├── data/
│   │   └── raw/
│   │       └── debug_cad.png
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── def_region.py
│   │   ├── get_description_print.py
│   │   ├── get_window.py
│   │   ├── organizer_tree.py
│   │   ├── paths.py
│   │   └── script_mouse.py
│   ├── __init__.py
│   ├── atualizar_dados_mes.py
│   ├── cad_verify.py
│   ├── get_description.py
│   ├── main.py
│   ├── main_ultimos_3_dias.py
│   └── organize.py
├── .gitignore
├── app.py
├── Automacao CAD.bat
├── README.md
└── requirements.txt

```

## 🚀 Como o Projeto Funciona (Fluxo de Dados)

1. O operador acessa o **Streamlit** e clica em "Sincronizar".
2. O Python assume o controle, foca no **CAD**, pesquisa as ocorrências de Passos e baixa o CSV.
3. O robô "mergulha" na última ocorrência, tira um print do histórico e usa **OCR** para ler o texto.
4. Os dados são compilados em uma planilha Excel formatada.
5. O operador escolhe a ocorrência no App e clica no botão de cópia (ou link direto) para enviar ao grupo de WhatsApp.

## ⚙️ Tecnologias Utilizadas

* **Python 3.x**
* **Streamlit** (Interface)
* **Pandas** (Tratamento de Dados)
* **PyAutoGUI & PyGetWindow** (RPA/Automação de UI)
* **Tesseract OCR** (Reconhecimento de Texto em Imagem)
* **Openpyxl** (Manipulação de Excel)

---

