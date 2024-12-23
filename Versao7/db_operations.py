import psycopg2
import warnings
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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


# def insert_data_into_main_table(data):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         sanitized_data = sanitize_data(data)
#         # print(f"Sanitized data: {sanitized_data[11]}", type(sanitized_data[11]))
#         cur.execute("""
#             INSERT INTO ocr_documentosocr (
#                 id_documento, email_usuario, num_op, ano_op, nome_original,
#                 arquivo, extensao_arquivo, pasta, caminho, conteudo,
#                 numero_pagina, arquivo_existe
#             )
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             ON CONFLICT (id_documento, nome_original) DO UPDATE
#             SET conteudo = EXCLUDED.conteudo,
#                     numero_pagina = EXCLUDED.numero_pagina,
#                     arquivo_existe = EXCLUDED.arquivo_existe,
#                     data_leitura = EXCLUDED.data_leitura
#         """, sanitized_data)
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#         print(f"Erro ao inserir dados: {e}")
#         raise e
#     finally:
#         cur.close()
#         conn.close()

# Essa função não está funcionando corretamente
# def insert_data_into_main_table(data):
#     """
#     Insere dados na tabela principal. Caso o conteúdo exceda o limite do tsvector, divide em múltiplas partes.

#     Args:
#         data (tuple): Dados a serem inseridos na tabela principal.

#     Returns:
#         None
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         # Dados recebidos
#         id_documento, email, num, ano, nome_original, arquivo, extensao, pasta, caminho, conteudo, numero_pagina, arquivo_existe = data

#         # Tamanho máximo para tsvector no PostgreSQL
#         max_tsvector_size = 1048575  # 1 MB em bytes

#         # Verifica se o conteúdo precisa ser dividido
#         if isinstance(conteudo, str) and len(conteudo.encode('utf-8')) > max_tsvector_size:
#             # Divide o conteúdo em partes menores
#             chunk_size = max_tsvector_size // 2  # Divisão conservadora
#             chunks = [conteudo[i:i + chunk_size] for i in range(0, len(conteudo), chunk_size)]
#             for idx, chunk in enumerate(chunks):
#                 # Adiciona um sufixo ao nome_original para identificar as partes
#                 nome_original_part = f"{nome_original}_part_{idx + 1}"
#                 cursor.execute(
#                     """
#                     INSERT INTO ocr_documentosocr (
#                         id_documento, email_usuario, num_op, ano_op, nome_original,
#                         arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina
#                     )
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """,
#                     (
#                         id_documento, email, num, ano, nome_original_part, arquivo, extensao,
#                         pasta, caminho, chunk, numero_pagina, arquivo_existe
#                     )
#                 )
#         else:
#             # Conteúdo não excede o limite, salva diretamente
#             cursor.execute(
#                 """
#                 INSERT INTO ocr_documentosocr (
#                     id_documento, email_usuario, num_op, ano_op, nome_original,
#                     arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina
#                 )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """,
#                 data
#             )

#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#         print(f"Erro ao inserir dados na tabela principal: {e}")
#         raise
#     finally:
#         cursor.close()
#         connection.close()

#Está funcionando parcialmente, pois ocorre erro durante arquivos grande - está salvando com o mesmo horário e fere a constraint
# def insert_data_into_main_table(data):
#     """
#     Insere dados na tabela principal. Caso o conteúdo exceda o limite do tsvector, divide em múltiplas partes.

#     Args:
#         data (tuple): Dados a serem inseridos na tabela principal.

#     Returns:
#         None
#     """

#     # Conecta ao banco de dados
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         # Dados recebidos
#         id_documento, email, num, ano, nome_original, arquivo, extensao, pasta, caminho, conteudo, page_number = data

#         # Dados a serem inseridos na tabela principal
#         # Tamanho máximo para tsvector no PostgreSQL
#         max_tsvector_size = 1048575  # 1 MB em bytes

#         # Verifica se o conteúdo precisa ser dividido
#         if isinstance(conteudo, str) and len(conteudo.encode('utf-8')) > max_tsvector_size:
#             # Divide o conteúdo em partes menores
#             chunk_size = max_tsvector_size // 2  # Divisão conservadora
#             chunks = [conteudo[i:i + chunk_size] for i in range(0, len(conteudo), chunk_size)]
#             for idx, chunk in enumerate(chunks):
#                 print(f"Inserindo parte {idx + 1} para nome_original: {nome_original}")
#                 # Salva cada parte com o mesmo nome_original
#                 cursor.execute(
#                     """
#                     INSERT INTO ocr_documentosocr (
#                         id_documento, email_usuario, num_op, ano_op, nome_original,
#                         arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina
#                     )
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """,
#                     (
#                         id_documento, email, num, ano, nome_original, arquivo, extensao,
#                         pasta, caminho, chunk, page_number
#                     )
#                 )
#         else:
#             # Conteúdo não excede o limite, salva diretamente
#             print(f"Inserindo conteúdo completo para nome_original: {nome_original}")
#             cursor.execute(
#                 """
#                 INSERT INTO ocr_documentosocr (
#                     id_documento, email_usuario, num_op, ano_op, nome_original,
#                     arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina
#                 )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """,
#                 data
#             )

#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#         print(f"Erro ao inserir dados no banco para nome_original: '{nome_original}'. Erro: {e}")
#         raise
#     finally:
#         cursor.close()
#         connection.close()


# def insert_data_into_main_table(data):
#     """
#     Insere dados na tabela principal. Caso o conteúdo exceda o limite do tsvector, divide em múltiplas partes.

#     Args:
#         data (tuple): Dados a serem inseridos na tabela principal.

#     Returns:
#         None
#     """
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         # Dados recebidos
#         id_documento, email, num, ano, nome_original, arquivo, extensao, pasta, caminho, conteudo, page_number = data

#         # Tamanho máximo para tsvector no PostgreSQL
#         max_tsvector_size = 1048575  # 1 MB em bytes

#         # Verifica se o conteúdo precisa ser dividido
#         if isinstance(conteudo, str) and len(conteudo.encode('utf-8')) > max_tsvector_size:
#             # Divide o conteúdo em partes menores
#             chunk_size = max_tsvector_size // 2  # Divisão conservadora
#             chunks = [conteudo[i:i + chunk_size] for i in range(0, len(conteudo), chunk_size)]

#             # Adiciona frações de milissegundos para diferenciar timestamps
#             base_time = datetime.now()
#             for idx, chunk in enumerate(chunks):
#                 fractional_time = base_time + timedelta(milliseconds=idx)
#                 cursor.execute(
#                     """
#                     INSERT INTO ocr_documentosocr (
#                         id_documento, email_usuario, num_op, ano_op, nome_original,
#                         arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
#                     )
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """,
#                     (
#                         id_documento, email, num, ano, nome_original, arquivo, extensao,
#                         pasta, caminho, chunk, page_number, fractional_time
#                     )
                    
#                 )
#         else:
#             # Conteúdo não excede o limite, salva diretamente
#             cursor.execute(
#                 """
#                 INSERT INTO ocr_documentosocr (
#                     id_documento, email_usuario, num_op, ano_op, nome_original,
#                     arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
#                 )
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """,
#                 data + (datetime.now(),)  # Adiciona o timestamp atual
#             )

#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#         print(f"Erro ao inserir dados no banco: {e}")
#         raise
#     finally:
#         cursor.close()
#         connection.close()


def insert_data_into_main_table(data):
    """
    Insere ou atualiza dados na tabela principal. Caso o conteúdo exceda o limite do tsvector, divide em múltiplas partes.

    Args:
        data (tuple): Dados a serem inseridos na tabela principal.

    Returns:
        None
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Dados recebidos
        id_documento, email, num, ano, nome_original, arquivo, extensao, pasta, caminho, conteudo, page_number = data
        #print(f"Extensão no arquivo - db_operations - : {extensao}")

        # Tamanho máximo para tsvector no PostgreSQL
        max_tsvector_size = 1048575  # 1 MB em bytes

        # Verifica se o conteúdo precisa ser dividido
        if isinstance(conteudo, str) and len(conteudo.encode('utf-8')) > max_tsvector_size:
            # Divide o conteúdo em partes menores
            chunk_size = max_tsvector_size // 2  # Divisão conservadora
            chunks = [conteudo[i:i + chunk_size] for i in range(0, len(conteudo), chunk_size)]

            for idx, chunk in enumerate(chunks):
                # Adiciona um sufixo ao nome_original para identificar as partes
                nome_original_chunk = f"{nome_original}_parte{idx + 1}"

                # Insere ou atualiza o chunk
                cursor.execute(
                #     """
                #     INSERT INTO ocr_documentosocr (
                #         id_documento, email_usuario, num_op, ano_op, nome_original,
                #         arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
                #     )
                #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                #     ON CONFLICT (id_documento, nome_original) DO UPDATE
                #     SET conteudo = CASE
                #         WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN EXCLUDED.conteudo
                #         ELSE ocr_documentosocr.conteudo
                #     END,
                #     data_leitura = CASE
                #         WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN NOW()
                #         ELSE ocr_documentosocr.data_leitura
                #     END
                #     """,
                #     (
                #         id_documento, email, num, ano, nome_original_chunk, arquivo, extensao,
                #         pasta, caminho, chunk, page_number
                #     )
                # )

                    """
                    INSERT INTO ocr_documentosocr (
                        id_documento, email_usuario, num_op, ano_op, nome_original,
                        arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (id_documento, nome_original) DO UPDATE
                    SET extensao_arquivo = EXCLUDED.extensao_arquivo,  -- Atualiza a extensão sempre
                        conteudo = CASE
                            WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN EXCLUDED.conteudo
                            ELSE ocr_documentosocr.conteudo
                        END,
                        data_leitura = CASE
                            WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN NOW()
                            ELSE ocr_documentosocr.data_leitura
                        END
                    """,
                    (
                        id_documento, email, num, ano, nome_original_chunk, arquivo, extensao,
                        pasta, caminho, chunk, page_number
                    )

                )
        else:
            #print(f"Extensão no arquivo - db_operations - else : {extensao}")
            # Conteúdo não excede o limite, salva diretamente
            cursor.execute(
            #     """
            #     INSERT INTO ocr_documentosocr (
            #         id_documento, email_usuario, num_op, ano_op, nome_original,
            #         arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
            #     )
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            #     ON CONFLICT (id_documento, nome_original) DO UPDATE
            #     SET conteudo = CASE
            #         WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN EXCLUDED.conteudo
            #         ELSE ocr_documentosocr.conteudo
            #     END,
            #     data_leitura = CASE
            #         WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN NOW()
            #         ELSE ocr_documentosocr.data_leitura
            #     END
            #     """,
            #     data
            # )
                """
                INSERT INTO ocr_documentosocr (
                    id_documento, email_usuario, num_op, ano_op, nome_original,
                    arquivo, extensao_arquivo, pasta, caminho, conteudo, numero_pagina, data_leitura
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (id_documento, nome_original) DO UPDATE
                SET extensao_arquivo = EXCLUDED.extensao_arquivo,  -- Atualiza a extensão sempre
                    conteudo = CASE
                        WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN EXCLUDED.conteudo
                        ELSE ocr_documentosocr.conteudo
                    END,
                    data_leitura = CASE
                        WHEN ocr_documentosocr.conteudo != EXCLUDED.conteudo THEN NOW()
                        ELSE ocr_documentosocr.data_leitura
                    END
                """,
                data
                )
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir dados no banco: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


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