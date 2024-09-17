import pandas as pd
from odf.opendocument import load
from odf.table import Table, Row, Cell


# Função para ler um arquivo ODF e retornar um DataFrame do Pandas
def read_odf(file_path):
    doc = load(file_path)
    table = doc.getElementsByType(Table)[0]  # Assumindo que há pelo menos uma tabela
    data = []
    for row in table.getElementsByType(Row):
        data.append([cell.value for cell in row.getElementsByType(Cell)])
    df = pd.DataFrame(data[1:], columns=data[0])  # Usando a primeira linha como cabeçalhos
    return df


def save_text_to_file(df, output_path):
    # Converte o DataFrame para uma string no formato CSV
    text = df.to_csv(index=False, sep='\t')  # Usando tabulação como delimitador
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Caminho para o arquivo ODF
odf_path = 'seu_arquivo.ods'
# Caminho para o arquivo de saída .txt
output_path = 'resultadoODF.txt'

# Lê o arquivo ODF e salva o conteúdo em um arquivo .txt
df_odf = read_odf(odf_path)
save_text_to_file(df_odf, output_path)

print(f"O conteúdo foi salvo em {output_path}")
