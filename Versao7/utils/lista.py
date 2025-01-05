# Supondo que os dados estejam em um arquivo JSON ou diretamente no formato de lista
import json

data = r"D:\Repositorios\ocr-api\Versao7\json_correcao\Json_errors.json"


# Carregar os dados do arquivo JSON
def extract_ids(data):
    """
    Extrai todos os IDs dos registros e os formata como uma string de tupla.

    :param data: Lista de dicionários contendo "ids_com_erro" no formato string com chaves.
    :return: String no formato ('id1', 'id2', ...)
    """

    with open(data, 'r') as file:
        data = json.load(file)

    # # Supondo que os dados estejam em um arquivo JSON
    # ids_array = []
    # for entry in data:
    #     # Remove as chaves e separa os IDs por vírgulas
    #     ids = entry["ids_com_erro"].strip("{} ").split(",")
    #     ids_array.extend(ids)

    # # Remove espaços em branco e monta o formato solicitado
    # formatted_ids = "(" + ", ".join(f"'{id.strip()}'" for id in ids_array) + ")"
    # return formatted_ids

    ids_array = []
    for entry in data:
        # Remove as chaves e separa os IDs por vírgulas
        ids = entry["ids_com_erro"].strip("{} ").split(",")
        ids_array.extend(id.strip() for id in ids)

    return ids_array


# Chamar a função para extrair os IDs
result = extract_ids(data)
print(len(result), result)
