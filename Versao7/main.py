import sys
import warnings
import os
import urllib3
from logging_report import generate_error_log, generate_extraction_summary_log
from extractors import extract_text_by_extension
from api_client import fetch_data_from_api
from db_operations import (
    insert_data_into_main_table,
    insert_error_into_table,
    create_table_if_not_exists,
    create_error_table_if_not_exists
)

sys.path.insert(0, './Versao7')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter("ignore", UserWarning)

START_PAGE = 22      # Número da página inicial
END_PAGE = 22         # Número da página final
DOCUMENT_ID = "571"   # ID do documento a ser processado (coloque o ID ou None) "93727"

MAX_PAGES = 20  # Define o número máximo de páginas a serem processadas


class ExtractionError(Exception):
    """Exceção específica para erros de extração de documentos."""


def save_data_to_db(data, page_number):
    """
    Salva os dados extraídos no banco de dados e gera logs de erros e sumário.

    Args:
        data (list): Lista de documentos a serem processados
        page_number (int): Número da página sendo processada

    Returns:
        None
    """
    total_registros = len(data)
    registros_sucesso = 0
    erros_extracao = []

    for item in data:
        print("Em 'save data to db'")
        _, extensao = os.path.splitext(item['arquivo'])
        extensao = extensao.lstrip('.').lower()

        try:
            conteudo, sucesso, erro_extracao = extract_text_by_extension(item['caminho'])
            if not sucesso:
                raise ExtractionError(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

            # Corrigido para tratar conteudo[0] que é a string do texto
            conteudo_texto = conteudo[0] if isinstance(conteudo, tuple) else conteudo
            conteudo_limpo = conteudo_texto.replace('\x00', '') if conteudo_texto else ''
            
            print("Inserindo dados no BD")
            insert_data_into_main_table((
                item['id_operacaodocumentos'], item['email'], item['numero'], item['ano'], item['nome'], item['arquivo'], extensao, item['pasta'],
                item['caminho'], conteudo_limpo, page_number
            ))
            registros_sucesso += 1

        except (ExtractionError, IOError, OSError) as e:
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


def process_page_range(page_start, page_end, doc_id=None):
    """
    Processa um intervalo de páginas e salva os dados no banco de dados.
    
    Args:
        page_start (int): Número da página inicial
        page_end (int): Número da página final
        doc_id (str, optional): ID do documento específico a ser processado
    """
    found = False
    for page_number in range(page_start, page_end + 1):
        print(f"Processando página {page_number}...")
        data = fetch_data_from_api(page_number=page_number)
        if data:
            if doc_id:
                print(f"Processando doc {doc_id} na página {page_number}...")
                # Filtrar o documento com o id_documento
                data_filtered = [item for item in data if item['id_operacaodocumentos'] == doc_id]
                if data_filtered:
                    save_data_to_db(data_filtered, page_number)
                    found = True
                    break
            else:
                save_data_to_db(data, page_number)
        else:
            print(f"Nenhum dado encontrado para a página {page_number}.")

    if doc_id and not found:
        print(f"Documento com ID {doc_id} não encontrado nas páginas especificadas.")


if __name__ == "__main__":
    create_table_if_not_exists()
    create_error_table_if_not_exists()

    if DOCUMENT_ID:
        # Se 'START_PAGE' e 'END_PAGE' não forem definidos, usamos valores padrão
        if not START_PAGE:
            START_PAGE = 1
        if not END_PAGE:
            END_PAGE = MAX_PAGES
        process_page_range(START_PAGE, END_PAGE, doc_id=DOCUMENT_ID)
    elif START_PAGE and END_PAGE:
        process_page_range(START_PAGE, END_PAGE)
    else:
        print("Por favor, defina 'START_PAGE' e 'END_PAGE', ou um 'DOCUMENT_ID'.")
