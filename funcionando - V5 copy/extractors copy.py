from io import BytesIO
import requests
import os
from extractors_utils import (
    extract_text_from_pdf,
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
    extract_text_from_pptx

)


def is_url(file_path):
    return file_path.startswith('http://') or file_path.startswith('https://')


def extract_text_by_extension(file_path, id_zip=None):
    """
        Função que determina a extração de conteúdo com base na extensão do arquivo.
    """
    # Verifica se é uma URL ou um arquivo local
    if is_url(file_path):
        try:
            response = requests.get(file_path, verify=False)
            response.raise_for_status()
            file_content = response.content  # Conteúdo binário do arquivo
            _, extension = os.path.splitext(file_path)
            extension = extension.lower().lstrip('.')
        except Exception as e:
            erro_msg = f"Erro ao baixar o arquivo da URL: {e}"
            print(erro_msg)
            return "", False, erro_msg
    else:
        _, extension = os.path.splitext(file_path)
        extension = extension.lower().lstrip('.')
        file_content = file_path  # Caminho do arquivo local

    # Verifica a extensão e chama a função apropriada
    try:
        if extension == 'csv':
            return extract_text_from_csv(file_content)
        elif extension == 'txt':
            return extract_text_from_txt(file_content), True, None
        elif extension in ['xlsx', 'xls']:
            return extract_text_from_xlsx(file_content), True, None
        elif extension == 'docx':
            return extract_text_and_images_from_docx(file_content), True, None
        elif extension == 'doc':
            return download_and_convert_doc_to_docx(file_path), True, None
        elif extension == 'pdf':
            if isinstance(file_content, bytes):
                return extract_text_from_pdf(BytesIO(file_content)), True, None

            else:
                with open(file_content, 'rb') as file:
                    return extract_text_from_pdf(file.read()), True, None
        elif extension in ['jpg', 'jpeg', 'png']:
            if isinstance(file_content, bytes):
                return extract_text_from_image(BytesIO(file_content)), True, None
            else:
                with open(file_content, 'rb') as file:
                    return extract_text_from_image(file.read()), True, None
        elif extension in ['html', 'htm']:
            return extract_text_from_html(file_content)
        elif extension == 'json':
            return extract_text_from_json(file_content)
        elif extension == 'xml':
            return extract_text_from_xml(file_content)
        elif extension in ['odt', 'ods', 'odp']:
            # Se for conteúdo binário, converte para BytesIO
            if isinstance(file_content, bytes):
                file_content = BytesIO(file_content)
            return (extract_text_from_odt(file_content) if extension == 'odt' else
                    extract_text_from_ods(file_content) if extension == 'ods' else
                    # extract_text_from_odg(file_content) if extension == 'odg' else
                    extract_text_from_odp(file_content)), True, None
        elif extension == 'odg':
            if isinstance(file_content, str):  # Se for caminho de arquivo local
                return extract_text_from_odg(file_content), True, None
            else:
                return extract_text_from_odg(BytesIO(file_content)), True, None  # Garante que seja um objeto tipo arquivo
        elif extension == 'pptx':
            if isinstance(file_content, bytes):
                return extract_text_from_pptx(BytesIO(file_content)), True, None
            else:
                return extract_text_from_pptx(file_content), True, None

        else:
            erro_msg = f"Extensão {extension} não suportada."
            #print(erro_msg)
            return "", False, erro_msg

    except Exception as e:
        erro_msg = f"Erro ao processar o arquivo com extensão {extension}: {e}"
        #print(erro_msg)
        return "", False, erro_msg
