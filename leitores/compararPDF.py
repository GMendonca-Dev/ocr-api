import fitz  # PyMuPDF
from difflib import unified_diff
from difflib import Differ


# def extract_text_from_pdf(pdf_path):
#     """Extrai o texto de cada página do PDF e retorna como lista de strings."""
#     text_by_page = []
#     with fitz.open(pdf_path) as pdf:
#         for page_num in range(pdf.page_count):
#             page = pdf[page_num]
#             text = page.get_text("text")
#             text_by_page.append(text)
#     return text_by_page


# def compare_pdfs(pdf1_path, pdf2_path, output_file=r"D:\Repositorios\ocr-api\leitores\diferencas.txt"):
#     """Compara o conteúdo dos PDFs página por página e salva as diferenças em um arquivo."""
#     pdf1_text = extract_text_from_pdf(pdf1_path)
#     pdf2_text = extract_text_from_pdf(pdf2_path)
    
#     with open(output_file, "w") as file:
#         for page_num, (text1, text2) in enumerate(zip(pdf1_text, pdf2_text), start=1):
#             if text1 != text2:
#                 file.write(f"Diferenças na página {page_num}:\n")
#                 for line in unified_diff(
#                     text1.splitlines(), text2.splitlines(),
#                     fromfile='PDF 1', tofile='PDF 2', lineterm=''
#                 ):
#                     file.write(line + "\n")
#                 file.write("\n" + "-"*80 + "\n")
#             else:
#                 file.write(f"Página {page_num} é igual nos dois PDFs.\n")
#                 file.write("\n" + "-"*80 + "\n")
#     print(f"Comparação concluída! Resultados salvos em {output_file}")


def extract_text_from_pdf(pdf_path):
    """Extrai o texto de cada página do PDF e retorna como lista de strings."""
    text_by_page = []
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text = page.get_text("text")
            text_by_page.append(text)
    return text_by_page


def compare_pdfs(pdf1_path, pdf2_path, output_file=r"D:\Repositorios\ocr-api\leitores\diferencas.txt"):
    """Compara o conteúdo dos PDFs página por página e salva apenas as diferenças em um arquivo."""
    pdf1_text = extract_text_from_pdf(pdf1_path)
    pdf2_text = extract_text_from_pdf(pdf2_path)
    differ = Differ()  # Cria o objeto para comparar linhas individualmente
    
    with open(output_file, "w") as file:
        for page_num, (text1, text2) in enumerate(zip(pdf1_text, pdf2_text), start=1):
            # Compara o texto das duas páginas e obtém apenas as diferenças
            diff = list(differ.compare(text1.splitlines(), text2.splitlines()))
            differences = [line for line in diff if line.startswith('- ') or line.startswith('+ ')]
            
            if differences:
                file.write(f"Diferenças na página {page_num}:\n")
                for line in differences:
                    file.write(line + "\n")
                file.write("\n" + "-"*80 + "\n")
            else:
                file.write(f"Nenhuma diferença encontrada na página {page_num}.\n")
                file.write("\n" + "-"*80 + "\n")
    
    print(f"Comparação concluída! Resultados salvos em {output_file}")

# Caminho dos seus PDFs
pdf1_path = r"D:\Repositorios\ocr-api\leitores\24_22_1300220 - V2.pdf"
pdf2_path = r"D:\Repositorios\ocr-api\leitores\24_22_1300220 - V3.pdf"

compare_pdfs(pdf1_path, pdf2_path)
