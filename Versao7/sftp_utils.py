from paramiko import Transport, SFTPClient
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env


# def file_exists_on_sftp(sftp_config, full_path):
#     """
#     Verifica se um arquivo existe no servidor SFTP.

#     Args:
#         sftp_config (dict): Configurações de conexão SFTP.
#         full_path (str): Caminho completo do arquivo no servidor SFTP.

#     Returns:
#         bool: True se o arquivo existir, False caso contrário.
#     """
#     try:
#         # Estabelece conexão com o servidor SFTP
#         transport = Transport((sftp_config['host'], int(sftp_config['port'])))
#         transport.connect(username=sftp_config['user'], password=sftp_config['password'])
#         sftp = SFTPClient.from_transport(transport)
#         print(f"Conectado ao SFTP: {sftp_config['host']}")

#         try:
#             # Usa o método as_posix() para garantir o formato correto do caminho no Linux
#             full_path_linux = Path(full_path).as_posix()
#             print(f"Verificando arquivo no caminho (Linux): {full_path_linux}")

#             # Usa o método stat para verificar a existência do arquivo diretamente
#             sftp.stat(full_path_linux)
#             print(f"Arquivo encontrado: {full_path_linux}")
#             return True
#         except FileNotFoundError:
#             print(f"Arquivo não encontrado: {full_path_linux}")
#             return False
#         finally:
#             sftp.close()
#             transport.close()
#     except Exception as e:
#         print(f"Erro ao conectar ao SFTP: {e}")
#         return False

# LOG_FILE_PATH = r"D:\Repositorios\ocr-api\Versao7\logs_sftps\sftp_file_check.txt"  # Caminho do arquivo de log
current_time = datetime.now().strftime("%d%m%Y_%H%M%S")
LOG_FILE_PATH = fr"D:\Repositorios\ocr-api\Versao7\logs_sftp\sftp_file_check_{current_time}.txt"


def file_exists_on_sftp(sftp_config, full_path):
    """
    Verifica se um arquivo existe no servidor SFTP e registra o resultado em um log.

    Args:
        sftp_config (dict): Configurações de conexão SFTP.
        full_path (str): Caminho completo do arquivo no servidor SFTP.

    Returns:
        bool: True se o arquivo existir, False caso contrário.
    """
    try:
        # Estabelece conexão com o servidor SFTP
        transport = Transport((sftp_config['host'], int(sftp_config['port'])))
        transport.connect(username=sftp_config['user'], password=sftp_config['password'])
        sftp = SFTPClient.from_transport(transport)
        
        try:
            # Usa o método as_posix() para garantir o formato correto do caminho no Linux
            full_path_linux = Path(full_path).as_posix()
            
            # Usa o método stat para verificar a existência do arquivo diretamente
            sftp.stat(full_path_linux)
            log_message = f"Arquivo encontrado : {full_path_linux}\n"
            append_to_log(log_message)
            return True
        except FileNotFoundError:
            log_message = f"Arquivo não encontrado : {full_path_linux}\n"
            append_to_log(log_message)
            return False
        finally:
            sftp.close()
            transport.close()
    except Exception as e:
        log_message = f"Erro ao conectar ao SFTP para o arquivo {full_path}: {e}\n"
        append_to_log(log_message)
        return False


def append_to_log(message):
    """
    Escreve uma mensagem no arquivo de log.

    Args:
        message (str): Mensagem a ser escrita no log.
    """
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(message)