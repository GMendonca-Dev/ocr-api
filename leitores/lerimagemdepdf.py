##### Funcionando a partir de arquivo local


# import fitz  # PyMuPDF
# import pytesseract
# from PIL import Image
# from io import BytesIO
# import urllib3

# #from warnings import simplefilter
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# # Configura o caminho para o executável do Tesseract se necessário (no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# def extract_text_from_image_pdf(pdf_path):
#     # Abre o arquivo PDF
#     doc = fitz.open(pdf_path)
#     all_text = ""
    
#     # Percorre cada página do PDF
#     for page_num in range(doc.page_count):
#         page = doc.load_page(page_num)
        
#         # Extrai a imagem da página como um objeto pixmap
#         pix = page.get_pixmap()
        
#         # Converte o pixmap para um objeto PIL Image
#         image = Image.open(BytesIO(pix.tobytes()))
        
#         # Realiza OCR na imagem para extrair o texto
#         ocr_text = pytesseract.image_to_string(image)
#         all_text += f"\nTexto extraído da página {page_num + 1}:\n{ocr_text}\n"
#         all_text += "-" * 40 + "\n"
    
#     return all_text


# def save_text_to_file(text, output_path):
#     with open(output_path, 'w', encoding='utf-8') as file:
#         file.write(text)


# # Caminho para o arquivo PDF
# pdf_path = r'D:\Repositorios\ocr-api\leitores\testepdf.pdf'
# # Caminho para o arquivo de saída .txtpython 
# output_path = r'D:\Repositorios\ocr-api\leitores\resultado.txt'

# # Extrai o texto do PDF (realizando OCR nas imagens)
# extracted_text = extract_text_from_image_pdf(pdf_path)

# # Salva o texto extraído no arquivo .txt
# save_text_to_file(extracted_text, output_path)

# print(f"O texto extraído foi salvo em {output_path}")

##### FIM Funcionando a partir de arquivo local



def extract_text_from_image_pdf(pdf_url):
    # Baixa o arquivo PDF da URL
    response = requests.get(pdf_url, verify=False)
    response.raise_for_status()  # Verifica se houve algum erro na requisição

    # Abre o PDF a partir do conteúdo baixado
    doc = fitz.open(stream=response.content, filetype="pdf")
    all_text = ""
    
    # Percorre cada página do PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # Extrai a imagem da página como um objeto pixmap
        pix = page.get_pixmap()
        
        # Converte o pixmap para um objeto PIL Image
        image = Image.open(BytesIO(pix.tobytes()))
        
        # Realiza OCR na imagem para extrair o texto
        ocr_text = pytesseract.image_to_string(image)
        all_text += f"\nPag {page_num + 1}:\n{ocr_text}\n"
        all_text += + "\n"
    
    return all_text


def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

# URL para o arquivo PDF
pdf_url = 'https://10.100.77.20/xpertis/App/Lib/arquivos/documentos/decisao/30_7_13022020130620_decisaoproc080026911.20197qst1.pdf'
# Caminho para o arquivo de saída .txt
output_path = r'D:\Repositorios\OCR-DOCUMENTOS\leitores\resultado.txt'

# Extrai o texto do PDF (realizando OCR nas imagens)
extracted_text = extract_text_from_image_pdf(pdf_url)

# Salva o texto extraído no arquivo .txt
save_text_to_file(extracted_text, output_path)

print(f"O texto extraído foi salvo em {output_path}")