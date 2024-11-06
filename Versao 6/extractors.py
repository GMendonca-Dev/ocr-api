from io import BytesIO
import requests
import os
import tempfile
from extractors_utils import (
    #extract_text_from_pdf,
    extract_text_from_txt,
    extract_text_from_xlsx,
    extract_text_and_images_from_docx,
    extract_text_from_image,
    download_and_convert_doc_to_docx,
    extract_text_from_html,
    extract_text_from_json,
    extract_text_from_csv,
    extract_text_from_odp,
    extract_text_from_odt,
    extract_text_from_ods,
    extract_text_from_odg,
    extract_text_from_xml,
    extract_text_from_pptx,
    extract_text_from_pdf_content

)

def extract_text_by_extension(file_path, id_zip=None):
    """
    Função que determina a extração de conteúdo com base na extensão do arquivo.
    """

    # Verifica se é uma URL ou um arquivo local
    if is_url(file_path):
        try:
            print(f"URL : {file_path}")  # Imprime a URL para verificação
            response = requests.get(file_path, verify=False)
            response.raise_for_status()
            _, extension = os.path.splitext(file_path)
            extension = extension.lower().lstrip('.')

            # Cria um arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extension}") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name  # Salva o caminho do arquivo temporário

            # Processa o arquivo salvo
            return process_file_by_extension(temp_file_path, extension)

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
        return process_file_by_extension(file_path, extension)

def process_file_by_extension(file_path, extension):
    """
    Processa o arquivo com base em sua extensão.
    """
    try:
        if extension == 'csv':
            return extract_text_from_csv(file_path)
        elif extension == 'txt':
            return extract_text_from_txt(file_path), True, None
        elif extension in ['xlsx', 'xls']:
            return extract_text_from_xlsx(file_path), True, None
        elif extension == 'docx':
            return extract_text_and_images_from_docx(file_path), True, None
        elif extension == 'doc':
            # Converte o .doc para .docx e processa
            docx_path = download_and_convert_doc_to_docx(file_path)
            return extract_text_and_images_from_docx(docx_path), True, None
        elif extension == 'pdf':
            return extract_text_from_pdf_content(file_path), True, None
        elif extension in ['jpg', 'jpeg', 'png']:
            return extract_text_from_image(file_path), True, None
        elif extension in ['html', 'htm']:
            return extract_text_from_html(file_path)
        elif extension == 'json':
            return extract_text_from_json(file_path)
        elif extension == 'xml':
            return extract_text_from_xml(file_path)
        elif extension in ['odt', 'ods', 'odp', 'odg']:
            return extract_text_from_odf(file_path, extension)
        elif extension == 'pptx':
            return extract_text_from_pptx(file_path), True, None
        else:
            erro_msg = f"Extensão {extension} não suportada."
            return "", False, erro_msg

    except Exception as e:
        erro_msg = f"Erro ao processar o arquivo com extensão {extension}: {e}"
        return "", False, erro_msg