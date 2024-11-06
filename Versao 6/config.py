import os
from dotenv import load_dotenv
import warnings
import pytesseract

# config.py
start_page = 10
end_page = 20

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)

# Caminho para o executável do Tesseract no Windows (path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Caminhos do LibreOffice e Tesseract
libreoffice_path = r"C:\Program Files\LibreOffice\program"
os.environ["PATH"] += os.pathsep + libreoffice_path
tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Adiciona LibreOffice ao PATH
os.environ["PATH"] += os.pathsep + libreoffice_path
os.environ["TESSERACT_CMD"] = tesseract_cmd

# Configurações da API
auth_url = os.getenv("AUTH_URL")
email = os.getenv("EMAIL")
senha = os.getenv("SENHA")
api_url = os.getenv("API_URL")
#page_number = int(input("Digite o número da página:"))

# Configurações do banco de dados
db_config = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("SENHA"),
    "host": os.getenv("HOST"),
    "port": int(os.getenv('PORT_DB'))
}
