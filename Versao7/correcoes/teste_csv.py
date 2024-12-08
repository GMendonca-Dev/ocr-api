from  import extract_text_and_images_from_docx
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
docx_path = r"D:\Repositorios\ocr-api\Versao7\csvs\48_34_1806202116_op108.2021telainfoimeidoimeiprincipal.docx"

# Extrai texto e imagens do arquivo DOCX
texto, sucesso, erro_msg = extract_text_and_images_from_docx(docx_path)

if sucesso:
    print("Texto completo extraído com sucesso:")
    print(texto)
else:
    print(f"Erro durante a extração: {erro_msg}")
