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
from dotenv import load_dotenv
from sftp_utils import file_exists_on_sftp
from pathlib import Path


load_dotenv()

sys.path.insert(0, './Versao7')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter("ignore", UserWarning)

START_PAGE = 1411      # Número da página inicial
END_PAGE = 1411        # Número da página final 
DOCUMENT_ID = "35691"   # ID do documento a ser processado (coloque o ID ou None) "93727"

# Parou na 1411 - Refazer


MAX_PAGES = 100  # Define o número máximo de páginas a serem processadas


class ExtractionError(Exception):
    """Exceção específica para erros de extração de documentos."""


# Sem a função sftp_utils.py
# def save_data_to_db(data, page_number):
#     """
#     Salva os dados extraídos no banco de dados e gera logs de erros e sumário.

#     Args:
#         data (list): Lista de documentos a serem processados
#         page_number (int): Número da página sendo processada

#     Returns:
#         None
#     """
#     total_registros = len(data)
#     registros_sucesso = 0
#     erros_extracao = []

#     for item in data:
#         #print("Em 'save data to db'")
#         _, extensao = os.path.splitext(item['arquivo'])
#         extensao = extensao.lstrip('.').lower()

#         # Verifica se o arquivo existe antes de tentar extrair o conteúdo
#         if not item.get('fileexists', 1):  # Se fileexists for 0 ou não existir
#             erro_msg = "Arquivo inexistente"
#             erros_extracao.append({**item, "erro": erro_msg})
#             insert_error_into_table((
#                 item['id_operacaodocumentos'], item['nome'], item['arquivo'], extensao, item['pasta'],
#                 item['caminho'], page_number, erro_msg, item['ano'], item['email'], item['numero'], item['fileexists']
#             ))
#             continue  # Pula para o próximo item sem tentar extrair o conteúdo

#         try:
#             conteudo, sucesso, erro_extracao = extract_text_by_extension(item['caminho'])
#             if not sucesso:
#                 raise ExtractionError(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

#             # Corrigido para tratar conteudo[0] que é a string do texto
#             conteudo_texto = conteudo[0] if isinstance(conteudo, tuple) else conteudo
#             conteudo_limpo = conteudo_texto.replace('\x00', '') if conteudo_texto else ''
#             print("Inserindo dados no BD")
#             # print(f"item['fileexists']:{item['fileexists']}")
#             insert_data_into_main_table((
#                 item['id_operacaodocumentos'], item['email'], item['numero'], item['ano'], item['nome'], item['arquivo'], extensao, item['pasta'],
#                 item['caminho'], conteudo_limpo, page_number, item['fileexists']
#             ))
#             registros_sucesso += 1

#         except (ExtractionError, IOError, OSError) as e:
#             erro_msg = str(e)
#             nome_original = item.get('nome')

#             erros_extracao.append({**item, "erro": erro_msg})
#             insert_error_into_table((
#                 item['id_operacaodocumentos'], nome_original, item['arquivo'], extensao, item['pasta'],
#                 item['caminho'], page_number, erro_msg, item['ano'],  item['email'], item['numero'], item['fileexists']
#             ))

#     if erros_extracao:
#         generate_error_log(page_number, erros_extracao, erro_msg)

#     generate_extraction_summary_log(page_number, total_registros, registros_sucesso, total_registros - registros_sucesso)

# Sem a função sftp_utils.py


def save_data_to_db(data, page_number):
    """
    Salva os dados extraídos no banco de dados e gera logs de erros e sumário.
    
    Args:
        data (list): Lista de documentos a serem processados.
        page_number (int): Número da página sendo processada.
    """

    print("Em 'save data to db'")
    total_registros = len(data)
    registros_sucesso = 0
    erros_extracao = []

    # Configurações do SFTP
    sftp_config = {
        "host": os.getenv("HOST_SFTP"),
        "port": int(os.getenv("PORT_SFTP")),  # Converte para inteiro
        "user": os.getenv("USER_SFTP"),
        "password": os.getenv("PASSWORD_SFTP"),
        "path_sftp": os.getenv("PATH_SFTP")
    }

    for item in data:
        _, extensao = os.path.splitext(item['arquivo'])
        extensao = extensao.lstrip('.').lower()

        # Valida se os campos necessários estão presentes
        if not sftp_config['path_sftp'] or not item['pasta'] or not item['arquivo']:
            erro_msg = "Caminho ou arquivo inválido"
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item['id_operacaodocumentos'], item['nome'], item['arquivo'] or '', extensao, item['pasta'] or '',
                '', page_number, erro_msg, item['ano'], item['email'], item['numero'], 0
            ))
            continue  # Pula para o próximo item

        # Construir o caminho completo do arquivo no servidor SFTP
        remote_path = Path(sftp_config['path_sftp']) / item['pasta'] / item['arquivo']

        #print(remote_path)  # Adicione esta linha antes de chamar file_exists_on_sftp

        # Verifica se o arquivo existe no servidor SFTP
        arquivo_existe = file_exists_on_sftp(sftp_config, str(remote_path))

        # Se o arquivo não existir, registra o erro e pula para o próximo item
        if not arquivo_existe:
            erro_msg = "Arquivo inexistente"
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item['id_operacaodocumentos'], item['nome'], item['arquivo'], extensao, item['pasta'],
                item['caminho'], page_number, erro_msg, item['ano'], item['email'], item['numero'], 0
            ))
            continue  # Pula para o próximo item sem tentar extrair o conteúdo

        # Tenta extrair o conteúdo do arquivo, caso falhe, registra o erro
    #     try:
    #         conteudo, sucesso, erro_extracao = extract_text_by_extension(str(remote_path))
    #         if not sucesso:
    #             raise ExtractionError(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

    #         conteudo_texto = conteudo[0] if isinstance(conteudo, tuple) else conteudo
    #         conteudo_limpo = conteudo_texto.replace('\x00', '') if conteudo_texto else ''
            
    #         insert_data_into_main_table((
    #             item['id_operacaodocumentos'], item['email'], item['numero'], item['ano'], item['nome'], item['arquivo'],
    #             extensao, item['pasta'], str(remote_path), conteudo_limpo, page_number, 1
    #         ))
    #         registros_sucesso += 1

    #     except (ExtractionError, IOError, OSError) as e:
    #         erro_msg = str(e)
    #         erros_extracao.append({**item, "erro": erro_msg})
    #         insert_error_into_table((
    #             item['id_operacaodocumentos'], item['nome'], item['arquivo'], extensao, item['pasta'],
    #             str(remote_path), page_number, erro_msg, item['ano'], item['email'], item['numero'], 1
    #         ))

    # if erros_extracao:
    #     generate_error_log(page_number, erros_extracao, erro_msg)

        try:
            conteudo, sucesso, erro_extracao = extract_text_by_extension(item['caminho'])
            if not sucesso:
                raise ExtractionError(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

            # Corrigido para tratar conteudo[0] que é a string do texto
            conteudo_texto = conteudo[0] if isinstance(conteudo, tuple) else conteudo
            conteudo_limpo = conteudo_texto.replace('\x00', '') if conteudo_texto else ''
            # print("Inserindo dados no BD")
            # print(f"item['fileexists']:{item['fileexists']}")
            insert_data_into_main_table((
                item['id_operacaodocumentos'], item['email'], item['numero'], item['ano'], item['nome'], item['arquivo'], extensao, item['pasta'],
                item['caminho'], conteudo_limpo, page_number, item['fileexists']
            ))
            registros_sucesso += 1

        except (ExtractionError, IOError, OSError) as e:
            erro_msg = str(e)
            nome_original = item.get('nome')
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item['id_operacaodocumentos'], nome_original, item['arquivo'], extensao, item['pasta'],
                item['caminho'], page_number, erro_msg, item['ano'],  item['email'], item['numero'], item['fileexists']
            ))

    if erros_extracao:
        generate_error_log(page_number, erros_extracao, erro_msg)

    # generate_extraction_summary_log(page_number, total_registros, registros_sucesso, total_registros - registros_sucesso)

    generate_extraction_summary_log(
        page_number,
        total_registros,
        registros_sucesso,
        total_registros - registros_sucesso
        )


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
                print(f"Processando doc: ID - {doc_id} na página Nº {page_number}...")
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
        print("Por favor, defina 'a página inicial' e a 'a página final', ou um 'DOCUMENT_ID'.")