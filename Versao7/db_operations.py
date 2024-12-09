import psycopg2
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)


def get_db_connection():
    return psycopg2.connect(
    #     dbname=db_config["dbname"],
    #     user=db_config["user"],
    #     password=db_config["password"],
    #     host=db_config["host"],
    #     port=db_config["port"]
    # )
        dbname=os.getenv("NAME_DB"),
        user=os.getenv("USER_DB"),
        password=os.getenv("PASSWORD_DB"),
        host=os.getenv("HOST_DB"),
        port=int(os.getenv('PORT_DB'))
    )


def clean_string(value):
    """
    Remove caracteres não imprimíveis de strings.
    """
    if isinstance(value, str):
        # Remove todos os caracteres não imprimíveis
        return ''.join(char for char in value if char.isprintable())
    return value


def sanitize_data(data):
    """
    Sanitiza todos os valores de uma tupla, removendo caracteres inválidos e convertendo bytes para str.
    """
    sanitized_data = []
    for idx, value in enumerate(data):
        if isinstance(value, bytes):
            print(f"Campo na posição {idx} é do tipo bytes. Convertendo para str.")
            value = value.decode('utf-8', errors='replace')
        if isinstance(value, str):
            if '\x00' in value:
                print(f"Campo na posição {idx} contém NUL antes da sanitização.")
            # Remove caracteres não imprimíveis
            cleaned_value = ''.join(c for c in value if c.isprintable())
            if '\x00' in cleaned_value:
                print(f"Campo na posição {idx} ainda contém NUL após sanitização.")
            sanitized_data.append(cleaned_value)
        else:
            sanitized_data.append(value)
    return tuple(sanitized_data)


def create_table_if_not_exists():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ocr_documentosocr (
                            
                        id VARCHAR(15) PRIMARY KEY,
                        id_documento VARCHAR(15),
                        email_usuario VARCHAR(50),
                        num_op VARCHAR(10),
                        ano_op VARCHAR(6),
                        nome_original VARCHAR(255),
                        arquivo VARCHAR(255),
                        extensao_arquivo VARCHAR(10),
                        pasta VARCHAR(255),
                        caminho TEXT,
                        arquivo_existe INT,
                        conteudo TEXT,
                        numero_pagina INT,
                        data_leitura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        # print("Tabela verificada ou criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")


def create_error_table_if_not_exists():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ocr_documentosocrerros (
                            
                        id VARCHAR(15) PRIMARY KEY,
                        id_documento VARCHAR(15) ,
                        nome_original VARCHAR(255),
                        arquivo VARCHAR(255),
                        extensao_arquivo VARCHAR(10),
                        pasta VARCHAR(255),
                        caminho TEXT,
                        arquivo_existe INT,
                        numero_pagina INT,
                        erro TEXT,
                        data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ano_op VARCHAR(6),
                        email_usuario VARCHAR(50),
                        num_op VARCHAR(10)
                        
                    )
                """)
        # print("Tabela de erros verificada ou criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela de erros: {e}")


def insert_data_into_main_table(data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        sanitized_data = sanitize_data(data)
        # print(f"Sanitized data: {sanitized_data[11]}", type(sanitized_data[11]))
        cur.execute("""
            INSERT INTO ocr_documentosocr (
                id_documento, email_usuario, num_op, ano_op, nome_original,
                arquivo, extensao_arquivo, pasta, caminho, conteudo,
                numero_pagina, arquivo_existe
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento, nome_original) DO UPDATE
            SET conteudo = EXCLUDED.conteudo,
                    numero_pagina = EXCLUDED.numero_pagina,
                    arquivo_existe = EXCLUDED.arquivo_existe,
                    data_leitura = EXCLUDED.data_leitura
        """, sanitized_data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir dados: {e}")
        raise e
    finally:
        cur.close()
        conn.close()


def insert_error_into_table(error_data):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Sanitiza os dados antes da inserção
        sanitized_data = sanitize_data(error_data)

        cur.execute("""
            INSERT INTO ocr_documentosocrerros (
                    id_documento, nome_original, arquivo, extensao_arquivo,
                    pasta, caminho, numero_pagina, erro, ano_op,
                    email_usuario, num_op, arquivo_existe
                    )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento, nome_original) DO UPDATE
            SET erro = EXCLUDED.erro,
                    arquivo_existe = EXCLUDED.arquivo_existe,
                    data_insercao = EXCLUDED.data_insercao
        """,  sanitized_data)
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error inserting error data: {e}")  # Adiciona log para verificar o erro
        raise e
    finally:
        cur.close()
        conn.close()