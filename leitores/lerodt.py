# def extract_text_from_odt(file_path_or_content):
#     try:
#         # Garante que file_path_or_content seja tratado como um objeto de arquivo
#         if isinstance(file_path_or_content, str):
#             with open(file_path_or_content, 'rb') as f:
#                 zip_file = zipfile.ZipFile(f)
#         else:
#             zip_file = zipfile.ZipFile(file_path_or_content)

#         with zip_file.open('content.xml') as f:
#             tree = ET.parse(f)
#             root = tree.getroot()

#         text_elements = [elem.text for elem in root.iter() if elem.text is not None]
#         extracted_text = "\n".join(text_elements)
#         return extracted_text, True
#     except Exception as e:
#         erro_msg = f"Erro ao ler ou processar o arquivo ODT: {e}"
#         print(erro_msg)  # Exibe o erro no console
#         return "", False

# import zipfile
# from lxml import etree


# def extrair_texto_de_odt(caminho_arquivo_odt, caminho_arquivo_txt):
#     try:
#         texto_extraido = ''
#         with zipfile.ZipFile(caminho_arquivo_odt, 'r') as arquivo_odt:
#             # Verifica se o content.xml existe no arquivo ODT
#             if 'content.xml' in arquivo_odt.namelist():
#                 with arquivo_odt.open('content.xml') as arquivo_content:
#                     tree = etree.parse(arquivo_content)
#                     # Define os namespaces utilizados
#                     namespaces = {
#                         'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
#                         'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
#                     }
#                     # Extrai todo o texto do corpo do documento
#                     texto_nodes = tree.xpath('/office:document-content/office:body//text()', namespaces=namespaces)
#                     texto_extraido = ''.join(texto_nodes)
#                 # Salva o texto extraído no arquivo TXT
#                 with open(caminho_arquivo_txt, 'w', encoding='utf-8') as arquivo_txt:
#                     arquivo_txt.write(texto_extraido)
#                 print(f"O texto extraído foi salvo em {caminho_arquivo_txt}")
#             else:
#                 print("O arquivo content.xml não foi encontrado no ODT.")
#     except Exception as e:
#         print(f"Ocorreu um erro: {e}")


import zipfile
from lxml import etree


def extrair_texto_de_odt(caminho_arquivo_odt, caminho_arquivo_txt):
    """
    Extrai o texto de um arquivo ODT, respeitando as quebras de linha, e salva em um arquivo TXT.

    Parâmetros:
    caminho_arquivo_odt (str): O caminho para o arquivo ODT.
    caminho_arquivo_txt (str): O caminho para o arquivo TXT onde o texto extraído será salvo.

    Retorna:
    None
    """
    try:
        texto_extraido = ''
        with zipfile.ZipFile(caminho_arquivo_odt, 'r') as arquivo_odt:
            # Verifica se o content.xml existe no arquivo ODT
            if 'content.xml' in arquivo_odt.namelist():
                with arquivo_odt.open('content.xml') as arquivo_content:
                    tree = etree.parse(arquivo_content)
                    # Define os namespaces utilizados
                    namespaces = {
                        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
                    }
                    # Encontra todos os elementos de parágrafo
                    paragrafos = tree.xpath('//text:p', namespaces=namespaces)
                    for paragrafo in paragrafos:
                        # Extrai o texto do parágrafo, incluindo elementos de texto interno
                        texto_paragrafo = ''.join(paragrafo.xpath('.//text()', namespaces=namespaces))
                        texto_extraido += texto_paragrafo + '\n'
                # Salva o texto extraído no arquivo TXT
                with open(caminho_arquivo_txt, 'w', encoding='utf-8') as arquivo_txt:
                    arquivo_txt.write(texto_extraido)
                print(f"O texto extraído foi salvo em {caminho_arquivo_txt}")
            else:
                print("O arquivo content.xml não foi encontrado no ODT.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


caminho_arquivo_txt = r"D:\Repositorios\ocr-api\leitores\resultado.txt"
caminho = r"D:\Repositorios\ocr-api\leitores\testeodt.odt"
extrair_texto_de_odt(caminho, caminho_arquivo_txt)