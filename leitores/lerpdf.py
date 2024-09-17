# import fitz  # PyMuPDF
# import pytesseract
# from PIL import Image
# from io import BytesIO

# # Configura o caminho para o executável do Tesseract se necessário (no Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# def extract_text_from_pdf(pdf_path):
#     # Abre o arquivo PDF
#     doc = fitz.open(pdf_path)
#     all_text = ""
    
#     for page_num in range(doc.page_count):
#         page = doc.load_page(page_num)
        
#         # Extrai o texto embutido na página
#         text = page.get_text("text")
#         all_text += text
        
#         # Extrai as imagens da página
#         images = page.get_images(full=True)
#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_data = base_image["image"]
#             image = Image.open(BytesIO(image_data))
            
#             # Realiza OCR na imagem
#             ocr_text = pytesseract.image_to_string(image)
#             all_text += f"\nTexto extraído da imagem {img_index + 1} na página {page_num + 1}:\n{ocr_text}\n"
    
#     return all_text

# # Caminho para o arquivo PDF
# pdf_path = r"E:\Git\mapas-se\arquivos\Uploads\testedoc3.pdf"

# # Extrai o texto e realiza OCR nas imagens
# extracted_text = extract_text_from_pdf(pdf_path)

# # Exibe o texto extraído
# print(extracted_text)


import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO

# Configura o caminho para o executável do Tesseract se necessário (no Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    # Abre o arquivo PDF
    doc = fitz.open(pdf_path)
    all_text = ""
    
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        
        # Extrai o texto embutido na página
        text = page.get_text("text")
        all_text += text
        
        # Extrai as imagens da página
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_data = base_image["image"]
            image = Image.open(BytesIO(image_data))
            
            # Realiza OCR na imagem
            ocr_text = pytesseract.image_to_string(image)
            all_text += f"\nTexto extraído da imagem {img_index + 1} na página {page_num + 1}:\n{ocr_text}\n"
    
    return all_text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Caminho para o arquivo PDF
pdf_path = r"E:\Git\mapas-se\arquivos\Uploads\testedoc3.pdf"
# Caminho para o arquivo de saída .txt
output_path = 'resultado.txt'

# Extrai o texto e realiza OCR nas imagens
extracted_text = extract_text_from_pdf(pdf_path)

# Salva o texto extraído no arquivo .txt
save_text_to_file(extracted_text, output_path)

print(f"Texto extraído foi salvo em {output_path}")
