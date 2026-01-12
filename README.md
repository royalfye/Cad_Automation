# 🛡️ Cad Automation & Info Portal

Sistema de automação para extração, organização e visualização de dados do sistema CAD. O projeto utiliza Python para automação de tarefas repetitivas e Streamlit para fornecer uma interface intuitiva de monitoramento e disparos.

## 📁 Estrutura do Projeto



```text
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
├── app.py
├── Automacao CAD.bat
├── README.md
└── requirements.txt