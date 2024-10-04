import psycopg2
import warnings
#from config import db_config

# Suprime os avisos do tipo UserWarning, incluindo o aviso do openpyxl
warnings.simplefilter("ignore", UserWarning)


def get_db_connection():
    # return psycopg2.connect(
    #     dbname=db_config["dbname"],
    #     user=db_config["user"],
    #     password=db_config["password"],
    #     host=db_config["host"],
    #     port=db_config["port"]
    # )
    return psycopg2.connect(
        dbname="ocr",  # Nome do banco de dados
        user="postgres",  # Usuário
        password="Aa123456@",  # Senha
        host="10.100.77.25",  # IP do container ou host
        port="5432"  # Porta do PostgreSQL
    )


def create_table_if_not_exists():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documentos_ocr (
                        id_documento VARCHAR(15) PRIMARY KEY,
                        nome_original VARCHAR(255),
                        arquivo VARCHAR(255),
                        extensao_arquivo VARCHAR(10),
                        pasta VARCHAR(255),
                        caminho TEXT,
                        conteudo TEXT,
                        ocr BOOLEAN,
                        numero_pagina INT,
                        data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        print("Tabela verificada ou criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela: {e}")


def create_error_table_if_not_exists():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS documentos_ocr_erros (
                        id_documento VARCHAR(15) PRIMARY KEY,
                        nome_original VARCHAR(255),
                        arquivo VARCHAR(255),
                        extensao_arquivo VARCHAR(10),
                        pasta VARCHAR(255),
                        caminho TEXT,
                        numero_pagina INT,
                        erro TEXT,
                        data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        print("Tabela de erros verificada ou criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela de erros: {e}")


def insert_data_into_main_table(data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO documentos_ocr (id_documento, nome_original, arquivo, extensao_arquivo, pasta, caminho, conteudo, ocr, numero_pagina)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento) DO UPDATE
            SET conteudo = EXCLUDED.conteudo, ocr = EXCLUDED.ocr, numero_pagina = EXCLUDED.numero_pagina
        """, data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def insert_error_into_table(error_data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO documentos_ocr_erros (id_documento, nome_original, arquivo, extensao_arquivo, pasta, caminho, numero_pagina, erro)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento) DO NOTHING
        """, error_data)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
