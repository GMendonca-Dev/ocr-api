from django.contrib.postgres.search import SearchVector

##### CSV #####
import pandas as pd
##### CSV #####

##### PDF #####
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO
##### PDF #####


# def indexar_texto(documento):
#     documento.search_vector = SearchVector('texto_extraido', 'titulo')
#     documento.save()




# # Função para ler arquivos CSV
# def ler_csv(arquivo):
#     with open(arquivo, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             print(row)


# def read_csv(file_path):
#     df = pd.read_csv(file_path)
#     return df


# def save_text_to_file(df, output_path):
#     # Converte o DataFrame para uma string no formato CSV
#     text = df.to_csv(index=False, sep='\t')  # Usando tabulação como delimitador
#     with open(output_path, 'w', encoding='utf-8') as file:
#         file.write(text)


# # Caminho para o arquivo CSV
# csv_path = 'seu_arquivo.csv'
# # Caminho para o arquivo de saída .txt
# output_path = 'resultadoCSV.txt'

# # Lê o arquivo CSV e salva o conteúdo em um arquivo .txt
# df_csv = read_csv(csv_path)
# save_text_to_file(df_csv, output_path)

# print(f"O conteúdo foi salvo em {output_path}")

# # Fim função ler arquivos CSV



# Função para ler arquivos PDF

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
pdf_path = r"https:\/\/10.100.77.20\/xpertis\/App\/Lib\/arquivos\/documentos\/emailinformandosobredocumentosprontos\/OP_82_2024_EMAIL_DOC_PRONTO_OFICIO_2335.2024.pdf"
# Caminho para o arquivo de saída .txt
output_path = 'resultado.txt'

# Extrai o texto e realiza OCR nas imagens
extracted_text = extract_text_from_pdf(pdf_path)

# Salva o texto extraído no arquivo .txt
save_text_to_file(extracted_text, output_path)

print(f"Texto extraído foi salvo em {output_path}")

# Função para ler arquivos PDF