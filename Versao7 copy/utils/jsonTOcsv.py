import json
import csv

# Caminho dos arquivos
json_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\tiposDocumento.json"
csv_path = r"D:\Repositorios\ocr-api\Versao7\arquivosGerais\tiposDocumento.csv"

# Ler o JSON
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Criar e escrever no CSV
with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Escrever cabeçalho
    writer.writerow(["id_tipodocumento", "pasta"])

    # Escrever linhas
    for item in data:
        writer.writerow([item["id_tipodocumento"], item["pasta"]])

print(f"Arquivo CSV salvo em: {csv_path}")
