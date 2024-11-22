from docx import Document
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance, ImageOps
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import requests
from io import BytesIO, StringIO
import os
import zipfile
from pptx import Presentation
import pandas as pd
import pdfplumber
import warnings
import sys
from lxml import etree
from PIL import ImageFilter
import subprocess
import xlrd


# ######## Conversão de arquivos .doc para .docx ########
# from docx.document import Document as Document_docx
# from win32com.client import Dispatch
# ######## Fim da Conversão de arquivos .doc para .docx ########


sys.path.insert(0, './Versao7')

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)

# Caminho para o executável do Tesseract no Windows (path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminhos do LibreOffice e Tesseract
libreoffice_path = r"C:\Program Files\LibreOffice\program"

os.environ["PATH"] += os.pathsep + libreoffice_path

tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_xml(file_path_or_content):
    try:
        # Verifica se é conteúdo binário ou um caminho de arquivo
        if isinstance(file_path_or_content, bytes):
            # Converte bytes para string
            file_content = file_path_or_content.decode('utf-8')
        else:
            # Lê o arquivo diretamente do caminho fornecido
            with open(file_path_or_content, 'r', encoding='utf-8') as file:
                file_content = file.read()
        
        # Analisa o conteúdo XML
        root = ET.fromstring(file_content)

        # Função recursiva para extrair texto de todos os elementos XML
        def extract_text(element):
            text = element.text.strip() if element.text else ""
            for child in element:
                text += "\n" + extract_text(child)
            return text
        
        # Extrai o texto do XML
        extracted_text = extract_text(root)
        
        return extracted_text, True, ""  # Retorna o texto extraído e sucesso

    except ET.ParseError as parse_error:
        erro_msg = f"Erro ao analisar o XML: {parse_error}"
        print(erro_msg)
        return "", False, erro_msg
    except Exception as e:
        erro_msg = f"Erro ao ler ou processar o arquivo XML: {e}"
        print(erro_msg)
        return "", False, erro_msg


def extract_text_from_odt(file_path_or_content):
    try:
        # Abre o arquivo ODT a partir de um caminho ou de um objeto de arquivo
        if isinstance(file_path_or_content, str):
            # file_path_or_content é um caminho de arquivo
            zip_file = zipfile.ZipFile(file_path_or_content, 'r')
        else:
            # file_path_or_content é um objeto de arquivo
            zip_file = zipfile.ZipFile(file_path_or_content)

        # Verifica se o content.xml existe no arquivo ODT
        if 'content.xml' in zip_file.namelist():
            with zip_file.open('content.xml') as f:
                tree = etree.parse(f)
                # Define os namespaces utilizados
                namespaces = {
                    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
                    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
                }
                # Encontra todos os elementos de parágrafo
                paragrafos = tree.xpath('//text:p', namespaces=namespaces)
                extracted_text = ''
                for paragrafo in paragrafos:
                    # Extrai o texto do parágrafo, incluindo elementos de texto internos
                    texto_paragrafo = ''.join(paragrafo.xpath('.//text()', namespaces=namespaces))
                    extracted_text += texto_paragrafo + '\n'
            return extracted_text, True
        else:
            erro_msg = "O arquivo content.xml não foi encontrado no ODT."
            print(erro_msg)
            return "", False
    except Exception as e:
        erro_msg = f"Erro ao ler ou processar o arquivo ODT: {e}"
        print(erro_msg)  # Exibe o erro no console
        return "", False


# Extração de texto de arquivos ODS (LibreOffice Calc)
def extract_text_from_ods(file_path_or_content):
    try:
        # Garante que file_path_or_content seja tratado como um objeto de arquivo
        if isinstance(file_path_or_content, str):
            with open(file_path_or_content, 'rb') as f:
                zip_file = zipfile.ZipFile(f)
        else:
            zip_file = zipfile.ZipFile(file_path_or_content)
        
        # Abre o arquivo 'content.xml' dentro do ODS
        with zip_file.open('content.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

        # Inicializa uma lista para armazenar o conteúdo extraído das células
        cell_texts = []

        # Percorre os elementos de célula no arquivo ODS
        for cell in root.iter('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-cell'):
            # Verifica o conteúdo do texto dentro da célula
            text_content = ''.join(cell.itertext())
            if text_content:  # Adiciona o conteúdo apenas se não for vazio
                cell_texts.append(text_content)

        # Junta o conteúdo de todas as células em uma única string
        extracted_text = "\n".join(cell_texts)
        return extracted_text, True
    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo ODS: {e}")
        return "", False


# Extração de texto de arquivos ODP (LibreOffice Impress)
def extract_text_from_odp(file_path_or_content):
    try:
        # Garante que file_path_or_content seja tratado como um objeto de arquivo
        if isinstance(file_path_or_content, str):
            with open(file_path_or_content, 'rb') as f:
                zip_file = zipfile.ZipFile(f)
        else:
            zip_file = zipfile.ZipFile(file_path_or_content)

        with zip_file.open('content.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

        text_elements = [elem.text for elem in root.iter() if elem.text is not None]
        extracted_text = "\n".join(text_elements)
        return extracted_text, True
    except Exception as e:
        erro_msg = f"Erro ao ler ou processar o arquivo ODP: {e}"
        print(erro_msg)  # Exibe o erro no console
        return "", False


# Extração de texto de arquivos ODG (LibreOffice Draw)
def extract_text_from_odg(file_path_or_content):
    try:
        # Garante que file_path_or_content seja tratado como um objeto de arquivo
        if isinstance(file_path_or_content, str):
            with open(file_path_or_content, 'rb') as f:
                zip_file = zipfile.ZipFile(f)
        else:
            zip_file = zipfile.ZipFile(file_path_or_content)
        
        # Abre o arquivo 'content.xml' dentro do ODG
        with zip_file.open('content.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

        # Inicializa uma lista para armazenar o conteúdo extraído
        extracted_texts = []

        # Itera sobre todos os elementos de texto relevantes no arquivo ODG, incluindo texto dentro de tags aninhadas
        for elem in root.iter():
            # Verifica se o elemento possui texto (ou parte de texto) e o adiciona à lista
            if elem.text:
                extracted_texts.append(elem.text)
            if elem.tail:  # Também captura texto após a tag de fechamento
                extracted_texts.append(elem.tail)

        # Junta o conteúdo extraído em uma única string
        extracted_text = "\n".join(extracted_texts)
        return extracted_text, True
    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo ODG: {e}")
        return "", False


def extract_text_from_txt(file_path_or_content):
    try:
        if isinstance(file_path_or_content, bytes):
            resultado = file_path_or_content.decode('latin1')
        else:
            with open(file_path_or_content, 'r', encoding='latin1') as file:
                resultado = file.read()
        return resultado, True
    except Exception as e:
        print(f"Erro ao ler arquivo txt: {e}")
        return "", False


def extract_text_from_odf(file_path, extension):
    try:
        if extension == 'odt':
            return extract_text_from_odt(file_path), True, None
        elif extension == 'ods':
            return extract_text_from_ods(file_path), True, None
        elif extension == 'odp':
            return extract_text_from_odp(file_path), True, None
        elif extension == 'odg':
            return extract_text_from_odg(file_path), True, None
    except Exception as e:
        erro_msg = f"Erro ao processar arquivo ODF ({extension}): {e}"
        return "", False, erro_msg


# def extract_text_from_xlsx(file_path_or_content):

#     try:
#         if isinstance(file_path_or_content, bytes):
#             file_content = BytesIO(file_path_or_content)
#             df = pd.read_excel(file_content, engine='openpyxl')
#         else:
#             df = pd.read_excel(file_path_or_content, engine='openpyxl')
#         return df.to_string(), True
#     except Exception as e:
#         print(f"Erro ao ler arquivo xlsx: {e}")
#         return "", False





def extract_text_from_xlsx(file_path_or_content):
    """
    Extrai o texto de todas as planilhas de um arquivo .xlsx.

    Parâmetros:
    - file_path_or_content (str ou bytes): Caminho para o arquivo .xlsx ou conteúdo em bytes.

    Retorna:
    - texto_extraido (str): O texto extraído de todas as planilhas.

    Lança:
    - FileNotFoundError: Se o arquivo não existir.
    - ValueError: Se o arquivo não for um arquivo Excel válido.
    - TypeError: Se o parâmetro 'file_path_or_content' não for do tipo esperado.
    - Exception: Para outros erros inesperados.
    """
    if isinstance(file_path_or_content, bytes):
        # Conteúdo em bytes
        file_content = BytesIO(file_path_or_content)
        excel_file = file_content
    elif isinstance(file_path_or_content, str):
        # Caminho do arquivo
        if not os.path.exists(file_path_or_content):
            raise FileNotFoundError(f"O arquivo '{file_path_or_content}' não existe.")
        excel_file = file_path_or_content
    else:
        raise TypeError("O parâmetro 'file_path_or_content' deve ser um caminho de arquivo (str) ou conteúdo em bytes.")

    try:
        # Lê todas as planilhas do arquivo Excel
        df_dict = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
        texto_extraido = ''

        for nome_planilha, df in df_dict.items():
            texto_extraido += f"=== Planilha: {nome_planilha} ===\n"
            texto_extraido += df.to_string(index=False)
            texto_extraido += '\n\n'

        return texto_extraido

    except FileNotFoundError:
        # O arquivo não foi encontrado durante a leitura
        raise FileNotFoundError(f"O arquivo '{file_path_or_content}' não foi encontrado.")
    except ValueError as ve:
        # Erro ao ler o arquivo Excel
        raise ValueError(f"Erro ao ler o arquivo xlsx: {ve}")
    except Exception as e:
        # Outros erros inesperados
        raise Exception(f"Erro inesperado ao processar o arquivo: {e}")










def extract_text_from_xls(file_path):
  
    """
    Detecta o formato real do arquivo e extrai o texto.

    Parâmetros:
    caminho_arquivo_xls (str): Caminho para o arquivo de entrada.

    Retorna:
    str: Texto extraído do documento.
    """
    # Verifica o formato real do arquivo
    with open(file_path, 'rb') as f:
        inicio = f.read(1024).lower()

    try:
        if b'<html' in inicio or b'<table' in inicio:
            # Trata como HTML
            texto = extract_text_from_html(file_path)
        elif inicio.startswith(b'pk'):
            # Trata como XLSX (arquivo zip)
            texto = extract_text_from_xlsx(file_path)
        else:
            try:
                workbook = xlrd.open_workbook(file_path)
                texto = ''
                for sheet in workbook.sheets():
                    texto += f"=== Planilha: {sheet.name} ===\n"
                    for row_idx in range(sheet.nrows):
                        row = sheet.row_values(row_idx)
                        texto += ', '.join(map(str, row)) + '\n'
                # return texto
            except Exception as e:
                print(f"Erro ao extrair texto do XLS: {e}")
                raise e
        return texto
    except Exception as e:
        print(f"Erro ao extrair texto: {e}")
        raise e


def extract_text_from_csv(file_path_or_content):
    try:
        # Verifica se o conteúdo é binário (baixado de uma URL e não de um arquivo local)
        if isinstance(file_path_or_content, bytes):
            # Converte bytes para string usando StringIO
            file_content = StringIO(file_path_or_content.decode('utf-8'))
        else:
            # Se for um caminho local, abre o arquivo e lê o conteúdo
            file_content = file_path_or_content

        # Usa pandas para ler o CSV e convertê-lo em uma string
        df = pd.read_csv(file_content, on_bad_lines='skip')
        return df.to_string(), True, ""  # Retorna o conteúdo como string, status de sucesso e erro vazio
    except Exception as e:
        erro_msg = f"Erro ao ler arquivo CSV: {e}"
        print(erro_msg)
        return "", False, erro_msg


def extract_text_and_images_from_docx(file_path_or_content):
    try:
        if isinstance(file_path_or_content, bytes):
            doc = Document(BytesIO(file_path_or_content))
        else:
            doc = Document(file_path_or_content)

        all_text = ""
        extracted_text_from_images = []
        extracted_tables = []

        for para in doc.paragraphs:
            all_text += para.text + "\n"

        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)
            extracted_tables.append(table_data)

        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                image_data = rel.target_part.blob
                text_from_image = extract_text_from_image(image_data)
                if isinstance(text_from_image, str):
                    extracted_text_from_images.append(text_from_image)

        combined_text = all_text + "\n".join(extracted_text_from_images)
        combined_text += "\n\n" + "\n".join(str(table) for table in extracted_tables)

        return combined_text, True

    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo DOCX: {e}")
        return "", False


def download_and_convert_doc_to_docx(file_path, diretorio_saida=None):
    """
    Converte um arquivo .doc para .docx usando LibreOffice.

    Parâmetros:
    caminho_arquivo_doc (str): Caminho para o arquivo .doc de entrada.
    diretorio_saida (str, opcional): Diretório onde o arquivo convertido será salvo. 
                                     Se None, usa o diretório do arquivo original.

    Retorna:
    str: Caminho para o arquivo .docx convertido.
    """
    if diretorio_saida is None:
        diretorio_saida = os.path.dirname(file_path)
    
    try:
        # Executa o comando de conversão
        subprocess.run([
            'soffice',
            '--headless',
            '--convert-to', 'docx',
            file_path,
            '--outdir', diretorio_saida
        ], check=True)
        
        # Obtém o nome base do arquivo sem extensão
        nome_base = os.path.splitext(os.path.basename(file_path))[0]
        caminho_docx = os.path.join(diretorio_saida, f"{nome_base}.docx")
        
        if os.path.exists(caminho_docx):
            return caminho_docx
        else:
            raise FileNotFoundError(f"Arquivo convertido {caminho_docx} não encontrado.")
    
    except subprocess.CalledProcessError as e:
        print(f"Erro na conversão do arquivo: {e}")
        raise e


def extract_text_from_image(image_path):
    try:
        # Abre a imagem a partir do caminho
        image = Image.open(image_path)

        # Pré-processamento da imagem
        image = image.convert('L').resize((image.width * 2, image.height * 2), resample=Image.BICUBIC)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        image = image.point(lambda x: 0 if x < 140 else 255, '1')

        # Realizar OCR na imagem
        text = pytesseract.image_to_string(image, lang='por', config='--psm 5')

        return text, True

    except Exception as e:
        print(f"Erro ao realizar OCR na imagem: {e}")
        return "", False


def extract_text_from_html(file_path_or_content):
    try:
        if isinstance(file_path_or_content, bytes):
            # Se o conteúdo for bytes (Ex: no caso de uma URL), converte para string
            file_content = file_path_or_content.decode('utf-8')
        else:
            # Se for um caminho de arquivo local
            with open(file_path_or_content, 'r', encoding='utf-8') as file:
                file_content = file.read()

        soup = BeautifulSoup(file_content, 'html.parser')
        # Extrai todo o texto visível do HTML
        text = soup.get_text(separator="\n")
        return text, True, ""  # Adicionei uma string vazia como mensagem de erro
    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo HTML: {e}")
        return "", False, str(e)


def extract_text_from_json(file_path_or_content):
    try:
        if isinstance(file_path_or_content, bytes):
            file_content = json.loads(file_path_or_content.decode('utf-8'))
        else:
            with open(file_path_or_content, 'r', encoding='utf-8') as file:
                file_content = json.load(file)

        # Recorre ao conteúdo do JSON e converte tudo em uma string
        def extract_json_text(data, result=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    result += f"{key}: {extract_json_text(value)}\n"
            elif isinstance(data, list):
                for item in data:
                    result += extract_json_text(item) + "\n"
            else:
                result += str(data)
            return result

        extracted_text = extract_json_text(file_content)
        return extracted_text, True, ""  # Adicionei uma string vazia como mensagem de erro
    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo JSON: {e}")
        return "", False, str(e)


def extract_text_from_pptx(file_path_or_content):

    try:
        if isinstance(file_path_or_content, (bytes, BytesIO)):
            file_content = BytesIO(file_path_or_content) if isinstance(file_path_or_content, bytes) else file_path_or_content
        elif isinstance(file_path_or_content, str) and (file_path_or_content.startswith("http://") or file_path_or_content.startswith("https://")):
            response = requests.get(file_path_or_content)
            response.raise_for_status()
            file_content = BytesIO(response.content)
        else:
            file_content = open(file_path_or_content, 'rb')

        prs = Presentation(file_content)
        all_text = []

        # Itera sobre os slides para garantir a extração de texto de todos os slides
        for slide_num, slide in enumerate(prs.slides, start=1):
            slide_text = f"\n--- Slide {slide_num} ---\n"
            
            # Extrair o texto dos shapes
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slide_text += shape.text + "\n"

                # Verificar se o shape contém uma tabela
                if shape.has_table:
                    table_text = "\n[Tabela]\n"
                    for row in shape.table.rows:
                        row_text = "\t".join(cell.text for cell in row.cells)
                        table_text += row_text + "\n"
                    slide_text += table_text

            # Realizar OCR sobre imagens dentro dos slides
            for shape in slide.shapes:
                if hasattr(shape, "image") and shape.image is not None:
                    image_stream = io.BytesIO(shape.image.blob)
                    image = Image.open(image_stream)
                    ocr_text = pytesseract.image_to_string(image, lang='por')
                    slide_text += f"\n[Imagem OCR]:\n{ocr_text}\n"
            
            all_text.append(slide_text)

        # Junta todo o texto extraído dos slides
        extracted_text = "\n".join(all_text)
        return extracted_text, True

    except Exception as e:
        print(f"Erro ao ler ou processar o arquivo PPTX: {e}")
        return "", False

    finally:
        if isinstance(file_content, BytesIO) is False and not isinstance(file_path_or_content, bytes):
            file_content.close()


def enhance_image(image):
    """Melhora a imagem para OCR com nitidez e contraste."""
    image = image.convert("L")  # Converte para escala de cinza
    image = image.filter(ImageFilter.SHARPEN)  # Aumenta a nitidez
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Aumenta o contraste
    image = ImageOps.autocontrast(image)  # Ajusta o brilho e contraste automaticamente
    return image


def download_pdf(url):
    """Baixa o PDF da URL e verifica o conteúdo."""
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        # Assegura que todo o conteúdo foi baixado
        pdf_content = BytesIO(response.content)
        pdf_content.seek(0)  # Garante que o ponteiro está no início
        return pdf_content
    except Exception as e:
        print(f"Erro ao baixar o PDF: {e}")
        return None


def extract_text_from_pdf_content(file_path):

    """Extrai texto de PDFs pesquisáveis e não pesquisáveis, aplicando OCR."""
    all_text = ""

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        return "", False, f"O arquivo {file_path} não existe."

    # Primeira tentativa: extrair texto com pdfplumber
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        all_text += f"\nPágina {page_num + 1}:\n{page_text}\n"
                    else:
                        # Se não houver texto, aplica OCR na imagem da página
                        page_image = page.to_image(resolution=300).original
                        enhanced_image = enhance_image(page_image)
                        ocr_text = pytesseract.image_to_string(enhanced_image, lang='por')
                        all_text += f"\nPágina {page_num + 1} (OCR):\n{ocr_text}\n"
                except Exception as e:
                    print(f"Erro ao processar a página {page_num + 1}: {e}")
    except Exception as e:
        print(f"Erro ao abrir PDF com pdfplumber: {e}")

    # Fallback: PyMuPDF para PDFs com imagens embutidas
    try:
        doc = fitz.open(file_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            image = Image.open(BytesIO(pix.tobytes()))
            enhanced_image = enhance_image(image)

            try:
                ocr_text = pytesseract.image_to_string(enhanced_image, lang='por')
                all_text += f"\nImagem na página {page_num + 1}:\n{ocr_text}\n"
            except Exception as ocr_error:
                print(f"Erro ao realizar OCR na página {page_num + 1}: {ocr_error}")
    except Exception as e:
        print(f"Erro ao processar imagens do PDF: {e}")

    return all_text, True, None

