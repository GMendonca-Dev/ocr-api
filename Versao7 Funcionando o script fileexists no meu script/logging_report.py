import json
import os
from datetime import datetime
import sys


sys.path.insert(0, './Versao7')


def generate_error_log(page_number, data, erro, log_dir="logs_erros"):
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = f"ErrosExtracao_pag_{page_number}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path = os.path.join(log_dir, log_file)

        log_data = [
            {
                "id_documento": item['id_operacaodocumentos'],
                "pagina": page_number,
                "nome_original": item['nome'],
                "arquivo": item['arquivo'],
                "extensao": os.path.splitext(item['arquivo'])[1],
                "pasta": item['pasta'],
                "caminho": item['caminho'],
                "erro": erro,
                "arquivo_existe": item['fileexists'],
                "data_insercao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            for item in data
        ]

        with open(log_path, 'w', encoding='utf-8') as log_file:
            json.dump(log_data, log_file, ensure_ascii=False, indent=4)
        print(f"Log de erros gerado: {log_path}")

        # Gera o arquivo JSON separado com a página e IDs dos documentos com erro
        error_ids = [item['id_operacaodocumentos'] for item in data]
        error_summary = {
            "pagina": page_number,
            "ids_com_erro": error_ids
        }

        error_summary_file = os.path.join(log_dir, f"ErrorSummary_pag_{page_number}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(error_summary_file, 'w', encoding='utf-8') as summary_file:
            json.dump(error_summary, summary_file, ensure_ascii=False, indent=4)
        print(f"Resumo de erros gerado: {error_summary_file}")

    except Exception as e:
        print(f"Erro ao gerar log de erros: {e}")


def generate_extraction_summary_log(page_number, total_registros, registros_sucesso, registros_com_erro, log_dir="logs_extracao"):
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = f"ResumoExtracao_pag_{page_number}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path = os.path.join(log_dir, log_file)

        summary_data = {
            "pagina": page_number,
            "total_registros": total_registros,
            "registros_sucesso": registros_sucesso,
            "registros_com_erro": registros_com_erro,
            "data_extracao": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        with open(log_path, 'w', encoding='utf-8') as log:
            json.dump(summary_data, log, ensure_ascii=False, indent=4)

        print(f"Log de resumo da extração gerado: {log_path}")
    except Exception as e:
        print(f"Erro ao gerar log de resumo da extração: {e}")
