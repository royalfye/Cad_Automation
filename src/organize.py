import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"
DATA_DIR = ROOT_DIR / "data" / "chamadas_csv"


def formatar_excel(excel_file_path):
    wb = load_workbook(excel_file_path)
    ws = wb.active

    for col in ws.iter_cols(1, ws.max_column):
        column_length = max(len(str(cell.value)) for cell in col)
        column_length = max(column_length, len(col[0].value)) 
        adjusted_width = min(column_length + 2, 50) 
        ws.column_dimensions[col[0].column_letter].width = adjusted_width

        for cell in col:
            cell.alignment = Alignment(horizontal='left', vertical='center')
    
    for cell in ws[1]:
        cell.font = Font(bold=True)

    aplicar_formatacao_condicional(ws)
    aplicar_bordas(ws)

    wb.save(excel_file_path)

def aplicar_formatacao_condicional(ws):
    coluna_ala_idx = None
    for col in ws.iter_cols(1, ws.max_column):
        if col[0].value == 'ALA':
            coluna_ala_idx = col[0].column_letter
            break

    if coluna_ala_idx:
        cores = {
            '4ª': 'FF0000',  # vermelha
            '3ª': '00FF00',  # verde
            '2ª': 'FFFF00',  # amarela
            '1ª': '0000FF',  # azul
        }

        for cell in ws[coluna_ala_idx][1:]: 
            fill_color = cores.get(cell.value, None)
            if fill_color:
                cell.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                font_color = '000000' if cell.value == '2ª' else 'FFFFFF' 
                cell.font = Font(color=font_color)

def aplicar_bordas(ws):
    borda_preta = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.border = borda_preta 

def organizar_por_data(excel_file_path, coluna_data='Data/hora de criação'):
    try:
        df = pd.read_excel(excel_file_path)

        if coluna_data not in df.columns:
            print(f"Coluna '{coluna_data}' não encontrada no arquivo!")
            return

        df[coluna_data] = pd.to_datetime(df[coluna_data], dayfirst=True, errors='coerce')
        df = df.sort_values(by=coluna_data)
        df[coluna_data] = df[coluna_data].dt.strftime('%d/%m/%Y %H:%M')
        
        df.to_excel(excel_file_path, index=False)
        formatar_excel(excel_file_path)

        print(f"Arquivo '{excel_file_path.name}' organizado com sucesso!")
    except Exception as e:
        print(f"Erro ao organizar a planilha: {e}")

if __name__ == "__main__":
    target_file = DATA_DIR / "nova_planilha_ocorrencias.xlsx"
    
    organizar_por_data(target_file)