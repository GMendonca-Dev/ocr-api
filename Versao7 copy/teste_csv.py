from extractors_utils import extract_text_from_csv

file_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\OP_154_2022_HC_LIN_79996001524.xls"

# texto, sucesso, erro_msg = extract_text_from_csv(file_path)

# if sucesso:
#     with open("output.txt", "w", encoding="utf-8") as file:
#         file.write(texto)
#     print("Texto extraído com sucesso:")
#     #print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")


import pandas as pd
from openpyxl import load_workbook
import xlrd
import mimetypes
import os


def process_excel_file(file_path):
    """
    Lê todas as abas de um arquivo Excel (.xls ou .xlsx) e retorna o texto extraído.

    Args:
        file_path (str): Caminho para o arquivo Excel.

    Returns:
        str: Texto consolidado de todas as abas do arquivo ou mensagem de erro.
    """
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(file_path):
            return f"Erro: O arquivo {file_path} não foi encontrado."

        # Detecta o tipo do arquivo
        mime_type, _ = mimetypes.guess_type(file_path)
        texto = ""

        if mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            # Trata arquivos .xlsx
            print("Detectado formato XLSX.")
            workbook = load_workbook(filename=file_path, data_only=True)
            for sheet_name in workbook.sheetnames:
                texto += f"\n=== Aba: {sheet_name} ===\n"
                sheet = workbook[sheet_name]
                for row in sheet.iter_rows(values_only=True):
                    if any(row):  # Garante que pelo menos uma célula tem valor
                        texto += ", ".join(map(str, row)) + "\n"
            return texto.strip()

        elif mime_type == 'application/vnd.ms-excel':
            # Trata arquivos .xls
            print("Detectado formato XLS.")
            workbook = xlrd.open_workbook(file_path)
            for sheet in workbook.sheets():
                texto += f"\n=== Aba: {sheet.name} ===\n"
                for row_idx in range(sheet.nrows):
                    row = sheet.row_values(row_idx)
                    if any(row):  # Garante que pelo menos uma célula tem valor
                        texto += ", ".join(map(str, row)) + "\n"
            return texto.strip()

        else:
            return f"Erro: Formato do arquivo não reconhecido ({mime_type})."

    except xlrd.biffh.XLRDError as e:
        return f"Erro ao processar arquivo XLS: {e}"
    except Exception as e:
        return f"Erro ao processar arquivo: {e}"


def extract_text_from_xls(file_path):
    """
    Função mestre que tenta ler um arquivo como planilha ou similar.

    Args:
        file_path (str): Caminho para o arquivo XLS ou similar.

    Returns:
        str: Texto extraído do arquivo.
    """
    try:
        return process_excel_file(file_path)
    except Exception as e:
        return f"Erro ao processar arquivo: {e}"


# Testando o script
resultado = extract_text_from_xls(file_path)
with open(r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\output.txt", "w", encoding="utf-8") as file:
    file.write(resultado)
#print(resultado)





# Caminho para a imagem
#image_path = r"D:\Repositorios\ocr-api\Versao7\images\24_34_17022020084236-285.jpg"

# # Extrai o texto da imagem
# texto, sucesso, erro_msg = extract_text_from_image(image_path)

# if sucesso:
#     print("Texto extraído com sucesso:")
#     print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")


# Caminho para o arquivo DOCX
# docx_path = r"D:\Repositorios\ocr-api\Versao7\csvs\48_34_1806202116_op108.2021telainfoimeidoimeiprincipal.docx"

# # Extrai texto e imagens do arquivo DOCX
# texto, sucesso, erro_msg = extract_text_and_images_from_docx(docx_path)

# if sucesso:
#     print("Texto completo extraído com sucesso:")
#     print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")



# #Caminho ou conteúdo do arquivo ODT
# file_path = r"D:\Repositorios\ocr-api\Versao7\csvs\39_8_13022020130620_representacaoinicialop019.2020 (1).odt"

# # Extrai texto do arquivo
# texto, sucesso, erro_msg = extract_text_from_odt(file_path)

# if sucesso:
#     print("Texto extraído com sucesso:")
#     print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")


# import tempfile

# temp_dir = tempfile.gettempdir()
# print(f"Diretório temporário para o usuário atual: {temp_dir}")





# # Caminho para o arquivo PDF
# pdf_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\OP_39_2023_IP__IP 3838-2022.pdf"
# output_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais"

# # Extrai texto e imagens do arquivo DOCX
# texto, sucesso, erro_msg = extract_text_from_pdf_content(pdf_path)

# if sucesso:
#     with open(output_path + "output.txt", "w", encoding="latin1") as file:
#         file.write(texto)
#     # with open("output.txt", "w", encoding="utf-8") as file:
#     #     file.write(texto)
#     print("Texto completo extraído com sucesso:")
#     #print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")


# ods_path = r"D:\Repositorios\ocr-api\Versao7\csvs\OP_96_20222_OP_SENHA_VG__TIM2.ods"

# ods_extractor = ODSExtractor(ods_path)
# extracted_text, success, error = ods_extractor.process()

# if success:
#     print(extracted_text)
# else:
#     print(f"Erro: {error}")



# from docling.document_converter import DocumentConverter

# source = "caminho_ou_URL_do_documento"
# converter = DocumentConverter()
# result = converter.convert(source)
# print(result.document.export_to_markdown())
