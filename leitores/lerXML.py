import pandas as pd
import xml.etree.ElementTree as ET


def read_xml(file_path):
    # Parse o arquivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Assumindo que os dados estão em uma lista de elementos
    data = []
    columns = set()
    
    # Itera sobre os elementos e coleta os dados
    for elem in root:
        row_data = {}
        for child in elem:
            columns.add(child.tag)
            row_data[child.tag] = child.text
        data.append(row_data)
    
    # Cria um DataFrame a partir dos dados coletados
    df = pd.DataFrame(data, columns=sorted(columns))
    return df


def save_text_to_file(df, output_path):
    # Converte o DataFrame para uma string no formato CSV
    text = df.to_csv(index=False, sep='\t')  # Usando tabulação como delimitador
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Caminho para o arquivo XML
xml_path = 'seu_arquivo.xml'
# Caminho para o arquivo de saída .txt
output_path = 'resultadoXML.txt'

# Lê o arquivo XML e salva o conteúdo em um arquivo .txt
df_xml = read_xml(xml_path)
save_text_to_file(df_xml, output_path)

print(f"O conteúdo foi salvo em {output_path}")
