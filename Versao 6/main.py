# main.py

from api_client import fetch_data_from_api
from db_operations import (
    insert_data_into_main_table,
    insert_error_into_table,
    create_table_if_not_exists,
    create_error_table_if_not_exists
)
import warnings
from logging_report import generate_error_log, generate_extraction_summary_log
from extractors import extract_text_by_extension
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter("ignore", UserWarning)

# Defina as variáveis aqui
start_page = 3571      # Número da página inicial
end_page = 3571         # Número da página final
document_id = "90393"   # ID do documento a ser processado (coloque o ID ou None)

# Se quiser processar um documento específico, defina 'document_id' como o ID desejado
# Se quiser processar um intervalo de páginas, deixe 'document_id' como None e defina 'start_page' e 'end_page'

MAX_PAGES = 50  # Define o número máximo de páginas a serem processadas


def save_data_to_db(data, page_number):
    total_registros = len(data)
    registros_sucesso = 0
    erros_extracao = []

    for item in data:
        _, extensao = os.path.splitext(item['arquivo'])
        extensao = extensao.lstrip('.').lower()

        try:
            conteudo, sucesso, erro_extracao = extract_text_by_extension(item['caminho'])
            if not sucesso:
                raise Exception(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

            insert_data_into_main_table((
                item['id_operacaodocumentos'], item['email'], item['numero'], item['ano'], item['nome'], item['arquivo'], extensao, item['pasta'],
                item['caminho'], conteudo, page_number
            ))
            registros_sucesso += 1

        except Exception as e:
            erro_msg = str(e)
            nome_original = item.get('nome')

            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item['id_operacaodocumentos'], nome_original, item['arquivo'], extensao, item['pasta'],
                item['caminho'], page_number, erro_msg, item['ano'],  item['email'], item['numero']
            ))

    if erros_extracao:
        generate_error_log(page_number, erros_extracao, erro_msg)

    generate_extraction_summary_log(page_number, total_registros, registros_sucesso, total_registros - registros_sucesso)


def process_page_range(start_page, end_page, document_id=None):
    found = False
    for page_number in range(start_page, end_page + 1):
        print(f"Processando página {page_number}...")
        data = fetch_data_from_api(page_number=page_number)
        if data:
            if document_id:
                # Filtrar o documento com o id_documento
                data_filtered = [item for item in data if item['id_operacaodocumentos'] == document_id]
                if data_filtered:
                    save_data_to_db(data_filtered, page_number)
                    found = True
                    break  # Interrompe a busca após encontrar o documento
            else:
                save_data_to_db(data, page_number)
        else:
            print(f"Nenhum dado encontrado para a página {page_number}.")

    if document_id and not found:
        print(f"Documento com ID {document_id} não encontrado nas páginas especificadas.")


if __name__ == "__main__":
    create_table_if_not_exists()
    create_error_table_if_not_exists()

    if document_id:
        # Se 'start_page' e 'end_page' não forem definidos, usamos valores padrão
        if not start_page:
            start_page = 1
        if not end_page:
            end_page = MAX_PAGES
        process_page_range(start_page, end_page, document_id=document_id)
    elif start_page and end_page:
        process_page_range(start_page, end_page)
    else:
        print("Por favor, defina 'start_page' e 'end_page', ou um 'document_id'.")
