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
                        conteudo TEXT,
                        numero_pagina INT,
                        data_leitura TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
        #print("Tabela verificada ou criada com sucesso.")
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
                        numero_pagina INT,
                        erro TEXT,
                        data_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ano_op VARCHAR(6),
                        email_usuario VARCHAR(50),
                        num_op VARCHAR(10)
                        
                    )
                """)
        #print("Tabela de erros verificada ou criada com sucesso.")
    except Exception as e:
        print(f"Erro ao criar a tabela de erros: {e}")


def insert_data_into_main_table(data):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO ocr_documentosocr (id_documento, email_usuario, num_op, ano_op, nome_original, arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento, nome_original) DO UPDATE
            SET conteudo = EXCLUDED.conteudo, numero_pagina = EXCLUDED.numero_pagina
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
            INSERT INTO ocr_documentosocrerros (id_documento, nome_original, arquivo, extensao_arquivo, pasta, caminho, numero_pagina, erro, ano_op, email_usuario, num_op)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_documento, nome_original) DO NOTHING
        """, error_data)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
