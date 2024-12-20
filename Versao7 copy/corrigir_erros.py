import json
from pathlib import Path
from api_client import fetch_data_from_api
from main import save_data_to_db


# def process_from_json_list(json_path):
#     """
#     Processa documentos especificados em um arquivo JSON contendo uma lista de páginas e IDs.

#     Args:
#         json_path (str): Caminho para o arquivo JSON contendo páginas e os documentos com erro.

#     Returns:
#         None
#     """
#     # Verifica se o arquivo JSON existe
#     if not Path(json_path).exists():
#         print(f"Erro: O arquivo JSON '{json_path}' não existe.")
#         return

#     # Lê o JSON e valida o conteúdo
#     try:
#         with open(json_path, 'r', encoding='utf-8') as file:
#             data = json.load(file)

#         # Verifica se o conteúdo é uma lista
#         if not isinstance(data, list):
#             print(f"Erro: O conteúdo do arquivo JSON '{json_path}' não é uma lista válida.")
#             return

#     except json.JSONDecodeError as e:
#         print(f"Erro ao decodificar o JSON: {e}")
#         return
#     except Exception as e:
#         print(f"Erro inesperado ao ler o JSON: {e}")
#         return

#     # Processa cada entrada na lista
#     for entry in data:
#         try:
#             page_number = entry.get("pagina")
#             doc_ids = entry.get("ids_com_erro")

#             if page_number is None or not doc_ids:
#                 print(f"Erro: O item '{entry}' deve conter 'pagina' e 'ids_com_erro'.")
#                 continue

#             # Busca os dados da API para a página especificada
#             api_data = fetch_data_from_api(page_number=page_number)
#             if not api_data:
#                 print(f"Nenhum dado encontrado para a página {page_number}.")
#                 continue

#             # Filtra os documentos com base nos IDs fornecidos no JSON
#             filtered_data = [item for item in api_data if item['id_operacaodocumentos'] in doc_ids]

#             if not filtered_data:
#                 print(f"Nenhum documento encontrado na página {page_number} com os IDs fornecidos.")
#                 continue

#             # Processa os documentos filtrados
#             save_data_to_db(filtered_data, page_number)
#             print(f"Processamento concluído para a página {page_number} e IDs {doc_ids}.")

#         except Exception as e:
#             print(f"Erro ao processar a página {entry.get('pagina', 'desconhecida')}: {e}")


def process_from_json(json_path):
    """
    Processa documentos especificados em um arquivo JSON.

    Args:
        json_path (str): Caminho para o arquivo JSON contendo páginas e IDs com erro.

    Returns:
        None
    """
    # Verifica se o arquivo JSON existe
    if not Path(json_path).exists():
        print(f"Erro: O arquivo JSON '{json_path}' não existe.")
        return

    # Lê o JSON e valida o conteúdo
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Se o conteúdo for um dicionário, converte para uma lista
        if isinstance(data, dict):
            data = [data]

        # Valida se o conteúdo é uma lista
        if not isinstance(data, list):
            print(f"Erro: O conteúdo do arquivo JSON '{json_path}' não é uma lista ou dicionário válido.")
            return

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar o JSON: {e}")
        return
    except Exception as e:
        print(f"Erro inesperado ao ler o JSON: {e}")
        return

    # Processa cada entrada na lista
    for entry in data:
        try:
            page_number = entry.get("pagina")
            doc_ids = entry.get("ids_com_erro")

            if page_number is None or not doc_ids:
                print(f"Erro: O item '{entry}' deve conter 'pagina' e 'ids_com_erro'.")
                continue

            # Busca os dados da API para a página especificada
            api_data = fetch_data_from_api(page_number=page_number)
            if not api_data:
                print(f"Nenhum dado encontrado para a página {page_number}.")
                continue

            # Filtra os documentos com base nos IDs fornecidos no JSON
            filtered_data = [item for item in api_data if item['id_operacaodocumentos'] in doc_ids]

            if not filtered_data:
                print(f"Nenhum documento encontrado na página {page_number} com os IDs fornecidos.")
                continue

            # Processa os documentos filtrados
            save_data_to_db(filtered_data, page_number)
            print(f"Processamento concluído para a página {page_number} e IDs {doc_ids}.")

        except Exception as e:
            print(f"Erro ao processar a página {entry.get('pagina', 'desconhecida')}: {e}")

    print("Processamento total concluído.")


print("Iniciando processamento...")

if __name__ == "__main__":
    JSON_PATH = r"D:\Repositorios\ocr-api\Versao7\json_correcao\Json_errors.json"  # Substitua pelo caminho do seu arquivo JSON
    process_from_json(JSON_PATH)