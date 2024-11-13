import os
from win32com.client import Dispatch
from docx import Document
from docx.shared import Inches

# def convert_doc_to_docx(doc_path, output_path):
#     try:
#         # Abrir o documento .doc usando win32com
#         word = Dispatch("Word.Application")
#         doc = word.Documents.Open(doc_path)

#         # Salvar o documento como .docx
#         doc.SaveAs(output_path, FileFormat=16)  # 16 = wdFormatDocumentDefault
#         doc.Close()
#         word.Quit()

#         # Criar um novo documento .docx e adicionar o texto
#         document = Document(output_path)
#         document.save(output_path)

#         return output_path
#     except Exception as e:
#         print(f"Erro ao converter o arquivo {doc_path}: {e}")
#         return None


def convert_doc_to_docx(doc_path, output_path):
    try:
        word = Dispatch("Word.Application")
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(output_path, FileFormat=16)  # 16 = wdFormatDocumentDefault
        doc.Close()
        word.Quit()
        word = None
        return output_path
    except Exception as e:
        print(f"Erro ao converter o arquivo {doc_path}: {e}")
        return None
    

# Exemplo de uso
input_file = r"D:\Repositorios\ocr-api\Versao 6\temp\teste.doc"
output_file = r"D:\Repositorios\ocr-api\Versao 6\temp\arquivo_convertido.docx"
converted_file = convert_doc_to_docx(input_file, output_file)

if converted_file:
    print(f"Arquivo convertido com sucesso: {converted_file}")
else:
    print("Falha na conversão do arquivo.")
