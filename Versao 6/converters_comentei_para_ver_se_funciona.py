import os
import subprocess
import requests
import warnings

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)


def convert_doc_with_libreoffice(doc_path, output_format="docx", temp_dir="temp"):
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        output_file_path = os.path.join(temp_dir, f"arquivo_temp.{output_format}")
        command = ['soffice', '--headless', '--convert-to', output_format, doc_path, '--outdir', temp_dir]
        subprocess.run(command, check=True)
        if os.path.exists(output_file_path):
            return output_file_path
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def download_and_convert_doc_to_docx(url, temp_dir="temp"):
    try:
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        response = requests.get(url, verify=False)
        response.raise_for_status()
        temp_file_path = os.path.join(temp_dir, "arquivo_temp.doc")
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(response.content)
        docx_path = convert_doc_with_libreoffice(temp_file_path, "docx")
        return docx_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
