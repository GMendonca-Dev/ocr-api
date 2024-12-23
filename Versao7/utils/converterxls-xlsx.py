import xlrd
from openpyxl import Workbook

arquivo = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\OP_22_2023_OP_SENHA_VG_CLARO_P3_"
destino = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\OP_22_2023_OP_SENHA_VG_CLARO_P3_2.xlsx"


def convert_xls_to_xlsx(xls_file, xlsx_file):
    # Abra o arquivo .xls com xlrd
    """
    Converte um arquivo .xls para .xlsx

    :param xls_file: caminho para o arquivo .xls
    :param xlsx_file: caminho para o arquivo .xlsx a ser criado
    """
    workbook_xls = xlrd.open_workbook(xls_file)
    sheet_xls = workbook_xls.sheet_by_index(0)

    # Crie um novo arquivo .xlsx com openpyxl
    workbook_xlsx = Workbook()
    sheet_xlsx = workbook_xlsx.active

    # Copie os dados de .xls para .xlsx
    for row in range(sheet_xls.nrows):
        for col in range(sheet_xls.ncols):
            sheet_xlsx.cell(row=row+1, column=col+1, value=sheet_xls.cell_value(row, col))

    # Salve o novo arquivo .xlsx
    workbook_xlsx.save(xlsx_file)


# Exemplo de uso
convert_xls_to_xlsx(arquivo, destino)
print("Conversão concluída!")
