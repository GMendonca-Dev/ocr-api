from db_operations import get_db_connection  # Importa a função de conexão com o banco


def save_extracted_data(data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Substitua "nome_da_tabela" pelo nome da tabela no seu banco
                cur.execute("""
                    INSERT INTO nome_da_tabela (id_zip, nome_original, arquivo, extensao_arquivo, caminho, conteudo, data_extracao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    data["id_zip"], data["nome_original"], data["arquivo"], data["extensao_arquivo"],
                    data["caminho"], data["conteudo"], data["data_extracao"]
                ))
                conn.commit()
        print(f"Dados do arquivo {data['arquivo']} salvos com sucesso no banco.")
        
    except Exception as e:
        print(f"Erro ao salvar os dados do arquivo no banco: {e}")
