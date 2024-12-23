import json


def transformar_dados(dados):
    """
    Transforma os dados de um JSON com IDs no formato de string para listas de strings.
    
    :param dados: Lista de dicionários com 'pagina' e 'ids_com_erro'.
    :return: Lista transformada com 'ids_com_erro' em formato de lista.
    """
    transformados = []
    for item in dados:
        # Remove as chaves e separa os IDs por vírgula
        ids = item["ids_com_erro"].strip("{}").split(",")
        transformados.append({"pagina": item["pagina"], "ids_com_erro": ids})
    return transformados


# Carrega os dados de um arquivo JSON
arquivo_entrada = r"D:\Repositorios\ocr-api\Versao7\json_correcao\_SELECT_numero_pagina_AS_pagina_ARRAY_AGG_id_documento_AS_ids_co_202412231505.json"
arquivo_saida = r"D:\Repositorios\ocr-api\Versao7\json_correcao\Json_errors.json"

with open(arquivo_entrada, "r") as f:
    dados = json.load(f)

# Transformação
dados_transformados = transformar_dados(dados)

# Salva os dados transformados em um novo arquivo JSON
with open(arquivo_saida, "w") as f:
    json.dump(dados_transformados, f, indent=4)

print(f"Dados transformados salvos em: {arquivo_saida}")

