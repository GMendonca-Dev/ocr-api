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
from utils.sftp_utils import file_exists_on_sftp
from pathlib import Path


load_dotenv()

sys.path.insert(0, './Versao7')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.simplefilter("ignore", UserWarning)

START_PAGE = 3938      # Número da página inicial 
END_PAGE = 3993       # Número da página final # parei na 
DOCUMENT_ID = None   # ID do documento a ser processado (coloque o ID ou None) "93727"

# Pasta 'oficiosadministrativos' já resolvido - Transferi o conteúdo da pasta oficiosadministrativos_old para oficiosadministrativos

MAX_PAGES = 300  # Define o número máximo de páginas a serem processadas


class ExtractionError(Exception):
    """Exceção específica para erros de extração de documentos."""


# Save data to db Novo, após o erro de tamanho max do campo to_tsvector
def save_data_to_db(data, page_number):
    """
    Salva os dados extraídos no banco de dados e gera logs de erros e sumário.
    
    Args:
        data (list): Lista de documentos a serem processados.
        page_number (int): Número da página sendo processada.
    """
    # print("Em 'save data to db'")
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
        # Mapeamento de campos
        nome_original = item.get('nome')  # Nome original do arquivo
        extensao = item['arquivo'].split('.')[-1].lower() if item.get('arquivo') else ''
        caminho_completo = item.get('caminho')
        arquivo_existe = item.get('fileexists', 0)
        # print(f"Extensão obtida do caminho: {extensao}")
        if extensao is None or extensao == '' and nome_original is not None:
            file_path = Path(nome_original)
            extensao = file_path.suffix.split('.')[-1].lower()
            # print(f"Extensão obtida do nome original: {extensao}")

        # # Verifica se a extensão está vazia e se o nome_original não é None ou vazio
        # if not extensao and nome_original:  
        #     extensao = nome_original.split('.')[-1].lower() # Se extensão não existir, tenta obter a extensão do nome original
        #     print(f"Nova extensão: {extensao}")

        # Valida se os campos necessários estão presentes
        if not sftp_config['path_sftp'] or not item.get('pasta') or not item.get('arquivo'):
            erro_msg = "Caminho ou arquivo inválido"
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item.get('id_operacaodocumentos'), nome_original, item.get('arquivo', ''), extensao,
                item.get('pasta', ''), '', page_number, erro_msg, item.get('ano'), item.get('email'),
                item.get('numero'), arquivo_existe
            ))
            continue  # Pula para o próximo item

        # Construir o caminho completo do arquivo no servidor SFTP
        remote_path = Path(sftp_config['path_sftp']) / item['pasta'] / item['arquivo']

        # Verifica se o arquivo existe no servidor SFTP
        if not file_exists_on_sftp(sftp_config, str(remote_path)):
            erro_msg = "Arquivo inexistente"
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item.get('id_operacaodocumentos'), nome_original, item['arquivo'], extensao,
                item['pasta'], caminho_completo, page_number, erro_msg, item['ano'], item['email'],
                item['numero'], arquivo_existe
            ))
            continue  # Pula para o próximo item

        # Tenta extrair o conteúdo do arquivo, caso falhe, registra o erro
        try:
            # print(f"Extensão no bloco de extração de caracteres : {extensao}")
            conteudo, sucesso, erro_extracao = extract_text_by_extension(caminho_completo, extensao)
            if not sucesso:
                raise ExtractionError(f"Falha ao processar {item['arquivo']}: {erro_extracao}")

            # Limpa o conteúdo extraído
            conteudo_texto = conteudo[0] if isinstance(conteudo, tuple) else conteudo
            conteudo_limpo = conteudo_texto.replace('\x00', '') if conteudo_texto else ''

            # print(f"Extensão a ser salva: {extensao}")  # Para depuração

            # # Insere no banco
            # insert_data_into_main_table((
            #     item.get('id_operacaodocumentos'), item.get('email'), item.get('numero'),
            #     item.get('ano'), nome_original, item.get('arquivo'), extensao, item.get('pasta'),
            #     caminho_completo, conteudo_limpo, page_number
            # ))
            # Certificar que 'id_tipodocumento' sempre tenha um valor válido
            id_tipo_documento = item.get('id_tipodocumento', "N/A")  # Se não existir, define "N/A"

            # Insere no banco, garantindo que 'id_tipo_documento' seja passado corretamente
            insert_data_into_main_table((
                item.get('id_operacaodocumentos'), item.get('email'), item.get('numero'),
                item.get('ano'), nome_original, item.get('arquivo'), extensao, item.get('pasta'),
                id_tipo_documento, caminho_completo, conteudo_limpo, page_number #, arquivo_existe  # 🔹 Adicionado arquivo_existe
            ))
            registros_sucesso += 1

        except (ExtractionError, IOError, OSError) as e:
            erro_msg = str(e)
            erros_extracao.append({**item, "erro": erro_msg})
            insert_error_into_table((
                item.get('id_operacaodocumentos'), nome_original, item.get('arquivo'), extensao,
                item.get('pasta'), caminho_completo, page_number, erro_msg, item.get('ano'),
                item.get('email'), item.get('numero'), arquivo_existe
            ))

    # Gera logs de erros e sumário
    if erros_extracao:
        generate_error_log(page_number, erros_extracao, erro_msg)

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
        # print(f"Processando página {page_number}...")
        data = fetch_data_from_api(page_number=page_number)
        if data:
            if doc_id:
                # print(f"Processando doc: ID - {doc_id} na página Nº {page_number}...")
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
