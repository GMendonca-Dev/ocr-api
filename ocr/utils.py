from django.contrib.postgres.search import SearchVector
import pandas as pd



def indexar_texto(documento):
    documento.search_vector = SearchVector('texto_extraido', 'titulo')
    documento.save()


class Leitores():

    # Documentos ".csv"
    def ler_csv(arquivo):
        with open(arquivo, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)


def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df


def save_text_to_file(df, output_path):
    # Converte o DataFrame para uma string no formato CSV
    text = df.to_csv(index=False, sep='\t')  # Usando tabulação como delimitador
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Caminho para o arquivo CSV
csv_path = 'seu_arquivo.csv'
# Caminho para o arquivo de saída .txt
output_path = 'resultadoCSV.txt'

# Lê o arquivo CSV e salva o conteúdo em um arquivo .txt
df_csv = read_csv(csv_path)
save_text_to_file(df_csv, output_path)

print(f"O conteúdo foi salvo em {output_path}")
