from extractors_utils import extract_text_from_odt, extract_text_from_pdf_content
# file_path = r"D:\Repositorios\ocr-api\Versao7\csvs\teste3_csv.csv"

# texto, sucesso, erro_msg = extract_text_from_csv(file_path)

# if sucesso:
#     print("Texto extraído com sucesso:")
#     print(texto)
# else:
#     print(f"Erro durante a extração: {erro_msg}")




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



# Caminho ou conteúdo do arquivo ODT
# file_path = r"D:\Repositorios\ocr-api\Versao7\csvs\3_representacaoinicial.odt"

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


# import os
# import tempfile


# def clear_temp_files(extensions_to_delete=None):
#     """
#     Remove arquivos específicos ou todos os arquivos da pasta Temp do Windows.

#     Args:
#         extensions_to_delete (list, optional): Lista de extensões de arquivo a serem excluídas. 
#                                                Se None, todos os arquivos serão excluídos.
    
#     Returns:
#         tuple: Número de arquivos excluídos, número de falhas.
#     """
#     temp_dir = tempfile.gettempdir()
#     deleted_count = 0
#     failed_count = 0

#     try:
#         for root, dirs, files in os.walk(temp_dir):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 try:
#                     # Verifica extensões se fornecido
#                     if extensions_to_delete:
#                         if not any(file.endswith(ext) for ext in extensions_to_delete):
#                             continue
                    
#                     # Apaga o arquivo
#                     os.remove(file_path)
#                     deleted_count += 1
#                 except Exception as e:
#                     print(f"Erro ao excluir {file_path}: {e}")
#                     failed_count += 1
#     except Exception as e:
#         print(f"Erro ao acessar a pasta Temp: {e}")

#     return deleted_count, failed_count


# extensions = ['.doc']  # Alterar para as extensões desejadas ou None para todos
# deleted, failed = clear_temp_files(extensions)
# print(f"Arquivos excluídos: {deleted}")
# print(f"Falhas: {failed}")


# Caminho para o arquivo PDF
pdf_path = r"D:\Repositorios\ocr-api\Versao7\csvs\24_22_13022020130620_oficio087.2020vivo+alvarade10.01.2020op167.19.pdf"

# Extrai texto e imagens do arquivo DOCX
texto, sucesso, erro_msg = extract_text_from_pdf_content(pdf_path)

if sucesso:
    print("Texto completo extraído com sucesso:")
    print(texto)
else:
    print(f"Erro durante a extração: {erro_msg}")
