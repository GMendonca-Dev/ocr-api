import logging
import time
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PipelineOptions,
    AcceleratorOptions,
    AcceleratorDevice,
    # TableStructureOptions
)
from docling.document_converter import DocumentConverter, ExcelFormatOption
from docling.pipeline.simple_pipeline import SimplePipeline
from docling.backend.msexcel_backend import MsExcelDocumentBackend


def conversao():
    logging.basicConfig(level=logging.INFO)

    # Configuração das opções de aceleração
    accelerator_options = AcceleratorOptions(
        num_threads=4,
        device=AcceleratorDevice.CUDA  # Define o uso da GPU NVIDIA
    )

    # Configuração das opções do pipeline para arquivos XLSX
    pipeline_options_xlsx = PipelineOptions(
        accelerator_options=accelerator_options
    )

    # Caminho para o documento de entrada
    input_doc_path = Path(r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\OP_213_2023_OP_SENHA_VG.xlsx")

    # Inicialização do conversor de documentos
    doc_converter = DocumentConverter(
        allowed_formats=[

                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX,
                InputFormat.ASCIIDOC,
                InputFormat.MD,
                InputFormat.XLSX,
            ],
        format_options={
            InputFormat.XLSX: ExcelFormatOption(
                pipeline_cls=SimplePipeline,
                pipeline_options=pipeline_options_xlsx,
                backend=MsExcelDocumentBackend
            )
            # InputFormat.XLSX: ExcelFormatOption(pipeline_options=pipeline_options_xlsx)
        }
    )

    # Conversão do documento
    start_time = time.time()
    conv_result = doc_converter.convert(input_doc_path)
    end_time = time.time() - start_time

    logging.info(f"Documento convertido em {end_time:.2f} segundos.")

    # Exportação dos resultados
    output_dir = Path(r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\csvs\csvsConvertidos")
    output_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = conv_result.input.file.stem

    # Exporta no formato Texto
    with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
        fp.write(conv_result.document.export_to_text())


conversao()



# from docling.document_converter import DocumentConverter

# Caminho para o arquivo PDF
# pdf_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\OP_39_2023_IP__IP 3838-2022.pdf"
# output_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais"


# pdf_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\pdfs\OP_39_2023_IP__IP 3838-2022.pdf"  # document per local path or URL
# converter = DocumentConverter()
# result = converter.convert(pdf_path)  # output: DocumentConverterResult(document, output_path)
# # with open(output_path + "output.txt", "w", encoding="latin1") as file:
# #     file.write(result.document.export_to_markdown())
# print(result.document.export_to_markdown())  # output: "## Docling Technical Report[...]"



# # Caminho para o arquivo PDF
# pdf_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\pdfs\paginasSeparadas\1_PDFsam_OP_39_2023_IP__IP 3838-2022 - Copia.pdf"
# # Caminho para salvar o arquivo de texto
# output_file = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\output.txt"

# # Inicializa o conversor de documentos
# converter = DocumentConverter()
# # Converte o PDF
# result = converter.convert(pdf_path)

# # Exporta o conteúdo convertido para Markdown
# markdown_content = result.document.export_to_markdown()

# # Salva o conteúdo em um arquivo de texto usando 'with open'
# with open(output_file, 'w', encoding='utf-8') as file:
#     file.write(markdown_content)

# print(f"Conteúdo salvo em {output_file}")


# import json
# import logging
# import time
# from pathlib import Path
# from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
# from docling.datamodel.base_models import InputFormat
# from docling.datamodel.pipeline_options import PdfPipelineOptions
# from docling.document_converter import DocumentConverter, PdfFormatOption
# from docling.models.ocr_mac_model import OcrMacOptions
# from docling.models.tesseract_ocr_cli_model import TesseractCliOcrOptions
# from docling.models.tesseract_ocr_model import TesseractOcrOptions


# _log = logging.getLogger(__name__)

# def conversao():

#     logging.basicConfig(level=logging.INFO)

#     # Explicitly set the accelerator
#     # accelerator_options = AcceleratorOptions(
#     #     num_threads=8, device=AcceleratorDevice.AUTO
#     # )
#     # accelerator_options = AcceleratorOptions(
#     #     num_threads=8, device=AcceleratorDevice.CPU
#     # )
#     # accelerator_options = AcceleratorOptions(
#     #     num_threads=8, device=AcceleratorDevice.MPS
#     # )
#     accelerator_options = AcceleratorOptions(
#         num_threads=8, device=AcceleratorDevice.CUDA
#     )

#     pipeline_options = PdfPipelineOptions()
#     pipeline_options.accelerator_options = accelerator_options

#     input_doc_path = Path("./tests/data/2206.01062.pdf")

#     ###########################################################################

#     # The following sections contain a combination of PipelineOptions
#     # and PDF Backends for various configurations.
#     # Uncomment one section at the time to see the differences in the output.

#     # PyPdfium without EasyOCR
#     # --------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = False
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = False

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(
#     #             pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
#     #         )
#     #     }
#     # )

#     # PyPdfium with EasyOCR
#     # -----------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = True
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(
#     #             pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
#     #         )
#     #     }
#     # )

#     # Docling Parse without EasyOCR
#     # -------------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = False
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     #     }
#     # )

#     # Docling Parse with EasyOCR
#     # ----------------------
#     pipeline_options = PdfPipelineOptions()
#     pipeline_options.do_ocr = True
#     pipeline_options.do_table_structure = True
#     pipeline_options.table_structure_options.do_cell_matching = True
#     pipeline_options.ocr_options.lang = ["es"]
#     pipeline_options.accelerator_options = AcceleratorOptions(
#         num_threads=4, device=Device.AUTO
#     )

#     doc_converter = DocumentConverter(
#         format_options={
#             InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#         }
#     )

#     # Docling Parse with EasyOCR (CPU only)
#     # ----------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = True
#     # pipeline_options.ocr_options.use_gpu = False  # <-- set this.
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     #     }
#     # )

#     # Docling Parse with Tesseract
#     # ----------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = True
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True
#     # pipeline_options.ocr_options = TesseractOcrOptions()

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     #     }
#     # )

#     # Docling Parse with Tesseract CLI
#     # ----------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = True
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True
#     # pipeline_options.ocr_options = TesseractCliOcrOptions()

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     #     }
#     # )

#     # Docling Parse with ocrmac(Mac only)
#     # ----------------------
#     # pipeline_options = PdfPipelineOptions()
#     # pipeline_options.do_ocr = True
#     # pipeline_options.do_table_structure = True
#     # pipeline_options.table_structure_options.do_cell_matching = True
#     # pipeline_options.ocr_options = OcrMacOptions()

#     # doc_converter = DocumentConverter(
#     #     format_options={
#     #         InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
#     #     }
#     # )

#     ###########################################################################

#     start_time = time.time()
#     conv_result = doc_converter.convert(input_doc_path)
#     end_time = time.time() - start_time

#     _log.info(f"Document converted in {end_time:.2f} seconds.")

#     ## Export results
#     output_dir = Path("scratch")
#     output_dir.mkdir(parents=True, exist_ok=True)
#     doc_filename = conv_result.input.file.stem

#     # Export Deep Search document JSON format:
#     with (output_dir / f"{doc_filename}.json").open("w", encoding="utf-8") as fp:
#         fp.write(json.dumps(conv_result.document.export_to_dict()))

#     # Export Text format:
#     with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
#         fp.write(conv_result.document.export_to_text())

#     # Export Markdown format:
#     with (output_dir / f"{doc_filename}.md").open("w", encoding="utf-8") as fp:
#         fp.write(conv_result.document.export_to_markdown())

#     # Export Document Tags format:
#     with (output_dir / f"{doc_filename}.doctags").open("w", encoding="utf-8") as fp:
#         fp.write(conv_result.document.export_to_document_tokens())


# import json
# import logging
# import time
# from pathlib import Path
# from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
# from docling.datamodel.base_models import InputFormat
# from docling.datamodel.pipeline_options import (
#     PdfPipelineOptions,
#     EasyOcrOptions,
#     AcceleratorOptions,
#     AcceleratorDevice
# )
# from docling.document_converter import DocumentConverter, PdfFormatOption

# _log = logging.getLogger(__name__)

# def conversao():
#     logging.basicConfig(level=logging.INFO)

#     # Configuração das opções do OCR
#     ocr_options = EasyOcrOptions(lang=["pt"])

#     # ##### Funcionando
    
#     # # Configuração das opções do pipeline
    # pipeline_options = PdfPipelineOptions(
    #     do_ocr=True,
    #     do_table_structure=True,
    #     table_structure_options=dict(do_cell_matching=True),
    #     ocr_options=ocr_options,
    #     accelerator_options=AcceleratorOptions(
    #         num_threads=4, device=AcceleratorDevice.AUTO
    #     )
    # )
#     # ######## Funcionando Fim


#     # Configuração das opções do pipeline
#     pipeline_options = PdfPipelineOptions(
#         do_ocr=True,
#         do_table_structure=True,
#         table_structure_options=dict(do_cell_matching=True),
#         ocr_options=ocr_options,
#         accelerator_options=AcceleratorOptions(
#             num_threads=4,
#             device=AcceleratorDevice.CUDA  # Define o uso da GPU NVIDIA
#         )
#     )

#     # Caminho para o documento de entrada
#     input_doc_path = Path(r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\docx\OP_90_2024_ANOT_AN_TELEMÁTICOS4.docx")

#     # Inicialização do conversor de documentos
#     doc_converter = DocumentConverter(
#         format_options={
#             InputFormat.PDF: PdfFormatOption(
#                 pipeline_options=pipeline_options,
#                 backend=PyPdfiumDocumentBackend,
#             )
#         }
#     )

#     # Conversão do documento
#     start_time = time.time()
#     conv_result = doc_converter.convert(input_doc_path)
#     end_time = time.time() - start_time

#     _log.info(f"Documento convertido em {end_time:.2f} segundos.")

#     # Exportação dos resultados
#     output_dir = Path(r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\pdfs\pdfsConvertidos3")
#     output_dir.mkdir(parents=True, exist_ok=True)
#     doc_filename = conv_result.input.file.stem

#     # # Exporta no formato JSON
#     # with (output_dir / f"{doc_filename}.json").open("w", encoding="utf-8") as fp:
#     #     json.dump(conv_result.document.export_to_dict(), fp, ensure_ascii=False, indent=4)

#     # Exporta no formato Texto
#     with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
#         fp.write(conv_result.document.export_to_text())

#     # # Exporta no formato Markdown
#     # with (output_dir / f"{doc_filename}.md").open("w", encoding="utf-8") as fp:
#     #     fp.write(conv_result.document.export_to_markdown())

#     # # Exporta no formato Document Tags
#     # with (output_dir / f"{doc_filename}.doctags").open("w", encoding="utf-8") as fp:
#     #     fp.write(conv_result.document.export_to_document_tokens())

# # if __name__ == "__main__":
# #     conversao()

# conversao()


