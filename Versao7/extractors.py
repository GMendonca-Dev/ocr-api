import requests
import os
import tempfile
# import json
import zipfile
import rarfile
import py7zr
import sys
from extractors_utils import (
    extract_text_from_txt,
    extract_text_from_xlsx,
    extract_text_from_xls,
    extract_text_from_xltx,
    extract_text_and_images_from_docx,
    extract_text_from_image,
    download_and_convert_doc_to_docx,
    extract_text_from_html,
    extract_text_from_json,
    extract_text_from_csv,
    extract_text_from_odf,
    extract_text_from_xml,
    extract_text_from_pptx,
    extract_text_from_pdf_content,
)
from db_operations import insert_data_into_main_table, insert_error_into_table

sys.path.insert(0, './Versao7')


def is_url(file_path):
    return file_path.startswith('http://') or file_path.startswith('https://')


def extract_compressed_file(file_path, temp_dir, original_data):
    """
    Extrai arquivos compactados recursivamente e processa cada arquivo.

    Args:
        file_path: Caminho do arquivo compactado
        temp_dir: Diretório temporário para extração
        original_data: Dados do arquivo compactado original
    """
    try:
        file_name = os.path.basename(file_path)

        # Cria subdiretório para este arquivo
        extract_dir = os.path.join(temp_dir, os.path.splitext(file_name)[0])
        os.makedirs(extract_dir, exist_ok=True)

        # Extrai baseado na extensão
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path) as zf:
                zf.extractall(extract_dir)
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path) as rf:
                rf.extractall(extract_dir)
        elif file_path.endswith('.7z'):
            with py7zr.SevenZipFile(file_path, mode='r') as sz:
                sz.extractall(extract_dir)

        # Processa todos os arquivos extraídos
        for root, _, files in os.walk(extract_dir):
            for file in files:
                current_file = os.path.join(root, file)

                # Se for outro arquivo compactado, extrai recursivamente
                if file.endswith(('.zip', '.rar', '.7z')):
                    extract_compressed_file(
                        current_file, temp_dir, original_data)
                else:
                    # Processa o arquivo para OCR
                    content, success, error = extract_text_by_extension(
                        current_file)

                    if success:
                        # Prepara dados para inserção mantendo dados originais
                        modified_data = original_data.copy()
                        # Atualiza apenas o nome
                        modified_data['nome_original'] = file

                        # Insere no banco de dados
                        insert_data_into_main_table((
                            modified_data['id_operacaodocumentos'],
                            modified_data['email'],
                            modified_data['numero'],
                            modified_data['ano'],
                            file,  # nome_original do arquivo interno
                            modified_data['arquivo'],
                            os.path.splitext(file)[1].lstrip('.'),
                            modified_data['pasta'],
                            modified_data['caminho'],
                            content,
                            modified_data.get('page_number', 1)
                        ))
                    else:
                        # Registra erro
                        insert_error_into_table((
                            modified_data['id_operacaodocumentos'],
                            file,  # nome_original do arquivo interno
                            modified_data['arquivo'],
                            os.path.splitext(file)[1].lstrip('.'),
                            modified_data['pasta'],
                            modified_data['caminho'],
                            modified_data.get('page_number', 1),
                            error,
                            modified_data['ano'],
                            modified_data['email'],
                            modified_data['numero']
                        ))

                # Remove o arquivo após processamento
                os.remove(current_file)

        # Remove o diretório de extração
        os.rmdir(extract_dir)

    except Exception as e:
        print(f"Erro ao processar arquivo compactado {file_path}: {e}")
        raise


def extract_text_by_extension(file_path, id_zip=None, original_data=None):
    """
    Função que determina a extração de conteúdo com base na extensão do arquivo.
    """
    if not file_path:
        erro_msg = "O caminho do arquivo é None."
        print(erro_msg)
        return "", False, erro_msg

    # Verifica se é uma URL ou um arquivo local
    if is_url(file_path):
        try:
            # print(f"URL : {file_path}")
            response = requests.get(file_path, verify=False, timeout=30)
            response.raise_for_status()
            _, extension = os.path.splitext(file_path)
            extension = extension.lower().lstrip('.')

            # Cria um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name  # Salva o caminho do arquivo temporário

            # Processa o arquivo salvo
            return process_file_by_extension(temp_file_path, extension, original_data)

        except Exception as e:
            erro_msg = f"Erro ao baixar o arquivo da URL: {e}"
            print(erro_msg)
            return "", False, erro_msg
        finally:
            # Remove o arquivo temporário após o processamento
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    else:
        _, extension = os.path.splitext(file_path)
        extension = extension.lower().lstrip('.')
        return process_file_by_extension(file_path, extension, original_data)


def process_file_by_extension(file_path, extension, original_data=None):
    """
    Processa o arquivo com base em sua extensão.
    """

    try:
        # Obtém o resultado da extração baseado na extensão
        if extension in ['zip', 'rar', '7z']:
            with tempfile.TemporaryDirectory() as temp_dir:
                extract_compressed_file(
                    file_path, temp_dir, original_data or {})
            return "Arquivo compactado processado com sucesso", True, None
            
        result = None
        # if extension == 'csv':
        #     result = extract_text_from_csv(file_path)
        if extension == 'csv':
            result = (extract_text_from_csv(file_path), True, None)
        elif extension == 'txt':
            result = (extract_text_from_txt(file_path)[0], True, None)
        elif extension == 'xlsx':
            result = (extract_text_from_xlsx(file_path), True, None)
        elif extension == 'xls':
            result = (extract_text_from_xls(file_path), True, None)
        elif extension == 'xltx':
            result = (extract_text_from_xltx(file_path), True, None)
        elif extension == 'docx':
            result = (extract_text_and_images_from_docx(file_path), True, None)
        elif extension == 'doc':
            # Converte o .doc para .docx e processa
            docx_path = download_and_convert_doc_to_docx(file_path)
            result = (extract_text_and_images_from_docx(docx_path), True, None)
        elif extension == 'pdf' or extension == '' or extension == "pdf'":
            result = (extract_text_from_pdf_content(file_path), True, None)
        elif extension in ['jpg', 'jpeg', 'png']:
            result = (extract_text_from_image(file_path), True, None)
        elif extension in ['html', 'htm']:
            result = (extract_text_from_html(file_path), True, None)
        elif extension == 'json':
            result = (extract_text_from_json(file_path), True, None)
        elif extension == 'xml':
            result = (extract_text_from_xml(file_path), True, None)
        elif extension in ['odt', 'ods', 'odp', 'odg']:
            result = (extract_text_from_odf(file_path, extension), True, None)
        elif extension == 'pptx':
            result = (extract_text_from_pptx(file_path), True, None)
        else:
            erro_msg = f"Extensão {extension} não suportada."
            return "", False, erro_msg

        # Verifica se o conteúdo extraído está vazio
        if result and result[0]:
            content = result[0]
            if isinstance(content, str) and not content.strip():
                return "", False, "Arquivo com conteúdo vazio"
            if isinstance(content, tuple) and not content[0].strip():
                return "", False, "Arquivo com conteúdo vazio"
            return result
        else:
            return "", False, "Arquivo com conteúdo vazio"

    except Exception as e:
        erro_msg = f"Erro ao processar o arquivo com extensão {extension}: {e}"
        return "", False, erro_msg
