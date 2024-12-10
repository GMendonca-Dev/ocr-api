import xml.etree.ElementTree as ET


def extract_text_pure(element, collected_text=None):
    """
    Extrai apenas o texto puro de um arquivo XML.

    Args:
        element (Element): Elemento XML raiz ou filho.
        collected_text (list): Lista para armazenar o texto extraído.

    Returns:
        str: Todo o texto puro extraído concatenado.
    """
    if collected_text is None:
        collected_text = []

    # Adiciona o texto do elemento, se existir
    if element.text and element.text.strip():
        collected_text.append(element.text.strip())

    # Processa os filhos do elemento
    for child in element:
        extract_text_pure(child, collected_text)

    # Adiciona o texto de tail, se existir (texto entre tags)
    if element.tail and element.tail.strip():
        collected_text.append(element.tail.strip())

    return " ".join(collected_text)


def read_xml_pure(file_path):
    """
    Lê um arquivo XML e retorna apenas o texto puro concatenado.

    Args:
        file_path (str): Caminho para o arquivo XML.

    Returns:
        str: Texto puro extraído do XML.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extrai todo o texto puro
    return extract_text_pure(root)


def save_text_to_file(text, output_path):
    """
    Salva o texto em um arquivo de texto.

    Args:
        text (str): Texto a ser salvo.
        output_path (str): Caminho para o arquivo de saída.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)


def xml():
    # Caminho para o arquivo XML
    xml_path = r"D:\Repositorios\ocr-api\Versao7\csvs\content.xml"
    # Caminho para o arquivo de saída .txt
    output_path = r"D:\Repositorios\ocr-api\Versao7\csvs\resultadoXML.txt"

    # Lê o texto puro do XML
    texto_puro = read_xml_pure(xml_path)

    # Salva o texto puro em um arquivo de saída
    save_text_to_file(texto_puro, output_path)

    print(f"O texto puro foi salvo em {output_path}")


xml()
