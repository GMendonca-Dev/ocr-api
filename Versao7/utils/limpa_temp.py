import os
import tempfile


def clear_temp_files(extensions_to_delete=None):
    """
    Remove arquivos específicos ou todos os arquivos da pasta Temp do Windows.

    Args:
        extensions_to_delete (list, optional): Lista de extensões de arquivo a serem excluídas. 
                                               Se None, todos os arquivos serão excluídos.
    
    Returns:
        tuple: Número de arquivos excluídos, número de falhas.
    """
    temp_dir = tempfile.gettempdir()
    deleted_count = 0
    failed_count = 0

    try:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Verifica extensões se fornecido
                    if extensions_to_delete:
                        if not any(file.endswith(ext) for ext in extensions_to_delete):
                            continue
                    
                    # Apaga o arquivo
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Erro ao excluir {file_path}: {e}")
                    failed_count += 1
    except Exception as e:
        print(f"Erro ao acessar a pasta Temp: {e}")

    return deleted_count, failed_count


extensions = ['.doc', '.pdf', '.doc', '.docx', '.odt', '.ods', '.csv', '.jpg', '.jpeg', '.png', '.zip', '.rar', '.7z', '.xlsx', '.xls', '.xltx', '.txt', '.anb']  # Alterar para as extensões desejadas ou None para todos
deleted, failed = clear_temp_files(extensions)
print(f"Arquivos excluídos: {deleted}")
print(f"Falhas: {failed}")