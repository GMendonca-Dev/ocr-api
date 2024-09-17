import pandas as pd


def read_excel(file_path):
    df = pd.read_excel(file_path, engine='openpyxl')  # Para XLSX
    return df


def save_text_to_file(df, output_path):
    # Converte o DataFrame para uma string no formato CSV
    text = df.to_csv(index=False, sep='\t')  # Usando tabulação como delimitador
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Caminho para o arquivo XLSX
excel_path = r'E:\Git\mapas-se\arquivos\Uploads\testexlsx.xlsx'
# Caminho para o arquivo de saída .txt
output_path = 'resultadoXLSX.txt'

# Lê o arquivo XLSX e salva o conteúdo em um arquivo .txt
df_excel = read_excel(excel_path)
save_text_to_file(df_excel, output_path)

print(f"O conteúdo foi salvo em {output_path}")
