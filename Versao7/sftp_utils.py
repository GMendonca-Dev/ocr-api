import paramiko


def file_exists_on_sftp(sftp_host, sftp_port, sftp_user, sftp_password, remote_path):
    """
    Verifica se um arquivo existe no servidor SFTP.
    
    Args:
        sftp_host (str): Endereço do servidor SFTP.
        sftp_port (int): Porta do servidor SFTP.
        sftp_user (str): Usuário para autenticação no SFTP.
        sftp_password (str): Senha para autenticação no SFTP.
        remote_path (str): Caminho completo do arquivo no servidor SFTP.
    
    Returns:
        bool: True se o arquivo existir, False caso contrário.
    """
    
    try:
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_user, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        try:
            sftp.stat(remote_path)
            return True  # O arquivo existe
        except FileNotFoundError:
            return False  # O arquivo não existe
        finally:
            sftp.close()
            transport.close()
    except Exception as e:
        print(f"Erro ao verificar o arquivo no SFTP: {e}")
        return False
