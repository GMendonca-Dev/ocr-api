import pyzipper


def extract_encrypted_zip(zip_path, extract_to, password):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.pwd = password.encode('utf-8')  # Configura a senha
            zf.extractall(path=extract_to)    # Extrai os arquivos
            print(f"Arquivos extraídos com sucesso para: {extract_to}")
    except RuntimeError as e:
        print(f"Erro ao extrair o arquivo ZIP: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


# Caminho para o arquivo ZIP e senha
zip_path = r"D:\Repositorios\ocr-api\Versao7\24_27_13022020130620_20.000122o.zip"
extract_to = r"D:\Repositorios\ocr-api\Versao7"
password = "oi31"

extract_encrypted_zip(zip_path, extract_to, password)
