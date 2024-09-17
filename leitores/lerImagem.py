# from PIL import Image
# import pytesseract

# # Configura o caminho para o executável do Tesseract se necessário (no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def extract_text_from_image(image_path):
#     # Abre a imagem
#     image = Image.open(image_path)
#     # Usa o Tesseract OCR para extrair o texto
#     text = pytesseract.image_to_string(image)
#     return text


# def save_text_to_file(text, output_path):
#     # Salva o texto extraído em um arquivo .txt
#     with open(output_path, 'w', encoding='utf-8') as file:
#         file.write(text)


# # Caminho para o arquivo de imagem
# image_path = r"E:\Git\mapas-se\Uploads\foto.jpg"  # Pode ser .jpeg, .png, .webm, etc.
# # Caminho para o arquivo de saída .txt
# output_path = 'resultadoImagem.txt'

# # Extrai o texto da imagem e salva em um arquivo .txt
# text = extract_text_from_image(image_path)
# save_text_to_file(text, output_path)

# print(f"O texto foi extraído e salvo em {output_path}")

import pytesseract
from PIL import Image


def extrair_texto_imagem(caminho_imagem):
  
    """
    Extrai o texto de uma imagem utilizando o Tesseract.

    Args:
        caminho_imagem: O caminho completo para a imagem.

    Returns:
        Uma string contendo o texto extraído da imagem.
    """

# Configuração do Tesseract (ajuste conforme necessário)
    custom_config = r'--oem 3 --psm 6'

# Carrega a imagem e extrai o texto
    try:
        texto = pytesseract.image_to_string(Image.open(caminho_imagem), config=custom_config)

        # Salva o texto em um arquivo .txt
        with open(nome_arquivo_saida + ".txt", "w", encoding='utf-8') as f:
            f.write(texto)
            print(f"Texto salvo em {nome_arquivo_saida}.txt")
    except Exception as e:
        print(f"Erro ao extrair texto: {e}")


# Exemplo de uso:
caminho_da_imagem = r"E:\Git\mapas-se\arquivos\Uploads\testepng.png"  # Substitua pelo caminho da sua imagem
nome_arquivo_saida = "texto_extraido"  # Nome do arquivo de saída

extrair_texto_imagem(caminho_da_imagem)