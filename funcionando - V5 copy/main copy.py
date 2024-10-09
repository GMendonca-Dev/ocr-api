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
from config import page_number
import os
import urllib3

#from warnings import simplefilter
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)


def save_data_to_db(data, page_number):
    #create_table_if_not_exists()
    #create_error_table_if_not_exists()

    total_registros = len(data)
    registros_sucesso = 0
    erros_extracao = []

    for item in data:

        # print("#############################################################################")
        # print(f"Erro ao extrair o conteúdo do item com ID: {item['id_operacaodocumentos']}")
        # print(f"Item com ID: {item['id_operacaodocumentos']}")
        # print(f"Nome original do arquivo: {item.get('nome')}")
        # print("#############################################################################")

        # Extrai a extensão do arquivo antes do bloco try-except (Adicionado aqui para evitar o erro de extensão de arquivo na tabela de erros)
        _, extensao = os.path.splitext(item['arquivo'])
        extensao = extensao.lstrip('.').lower()

        try:

            
            # _, extensao = os.path.splitext(item['arquivo'])
            # extensao = extensao.lstrip('.').lower()


            # Extrair o conteúdo
            conteudo, sucesso, erro_extracao = extract_text_by_extension(item['caminho'])
            if not sucesso:
                raise Exception(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

            insert_data_into_main_table((
                item['id_operacaodocumentos'], item['nome'], item['arquivo'], extensao, item['pasta'], 
                item['caminho'], conteudo, page_number
            ))
            registros_sucesso += 1

        except Exception as e:
            erro_msg = str(e)
            
            # Captura o nome original do arquivo
            nome_original = item.get('nome')
            if not nome_original:  # Se o nome não estiver presente, registrar uma mensagem de aviso
                # print("Nome original não encontrado")
                nome_original = "Nome original não encontrado"

            # Registra o erro na tabela de erros
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item['id_operacaodocumentos'], nome_original, item['arquivo'], extensao, item['pasta'], 
                item['caminho'], page_number, erro_msg
            ))

    if erros_extracao:
        generate_error_log(page_number, erros_extracao, erro_msg)

    generate_extraction_summary_log(page_number, total_registros, registros_sucesso, total_registros - registros_sucesso)


if __name__ == "__main__":
    data = fetch_data_from_api(page_number)
    if data:
        save_data_to_db(data, page_number)
