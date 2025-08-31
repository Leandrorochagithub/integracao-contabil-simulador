import os
import shutil
import pandas as pd
import pyodbc
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

PASTA_ENTRADA = r'G:\My Drive\personal\_studies\python\projects\accounting_automation\1_integration'
PASTA_PROCESSADOS = r'G:\My Drive\personal\_studies\python\projects\accounting_automation\1_integration\notas_processadas'

DB_SERVER = os.getenv('DB_SERVER')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# String de conexão montada com as variáveis de ambiente
DB_CONN_STR = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={DB_SERVER};'
    f'DATABASE={DB_DATABASE};'
    f'UID={DB_USER};'
    f'PWD={DB_PASSWORD};'
)

# --- FUNÇÕES ---

def verificar_pastas():
    """Garante que as pastas de entrada e de processados existam."""
    print("Verificando estrutura de pastas...")
    if not os.path.exists(PASTA_ENTRADA):
        os.makedirs(PASTA_ENTRADA)
    if not os.path.exists(PASTA_PROCESSADOS):
        os.makedirs(PASTA_PROCESSADOS)

def processar_arquivos_entrada():
    """
    Lê arquivos .csv da pasta de entrada, insere os dados no banco de dados
    e move os arquivos processados.
    """
    print("Procurando por novos arquivos de notas fiscais...")
    if not all([DB_SERVER, DB_DATABASE, DB_USER, DB_PASSWORD]):
        print("ERRO: Uma ou mais variáveis de ambiente do banco de dados não foram definidas no arquivo .env")
        return

    try:
        arquivos_csv = [f for f in os.listdir(PASTA_ENTRADA) if f.endswith('.csv')]

        if not arquivos_csv:
            print("Nenhum arquivo .csv encontrado para processar.")
            return

        print(f"Arquivos encontrados: {', '.join(arquivos_csv)}")
        
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        print(f"Conexão com o banco '{DB_DATABASE}' estabelecida com o usuário '{DB_USER}'.")

        for nome_arquivo in arquivos_csv:
            caminho_completo = os.path.join(PASTA_ENTRADA, nome_arquivo)
            print(f"\n--- Processando arquivo: {nome_arquivo} ---")

            try:
                df_notas = pd.read_csv(caminho_completo)
                for index, nota in df_notas.iterrows():
                    cnpj = nota['cnpj_cliente']
                    numero = int(nota['numero_nota'])
                    valor = float(nota['valor'])
                    data_emissao = nota['data_emissao']
                    
                    sql_insert = """
                        INSERT INTO NotasFiscais (ClienteCNPJ, NumeroNota, Valor, DataEmissao, Status, DataProcessamento)
                        VALUES (?, ?, ?, ?, ?, ?);
                    """
                    valores = (cnpj, numero, valor, data_emissao, 'Processado', datetime.now())
                    
                    cursor.execute(sql_insert, valores)
                    print(f"  - Nota Nº {numero} inserida no banco de dados.")

                conn.commit()
                shutil.move(caminho_completo, os.path.join(PASTA_PROCESSADOS, nome_arquivo))
                print(f"Arquivo '{nome_arquivo}' movido para a pasta de processados.")

            except Exception as e:
                print(f"  ERRO ao processar o arquivo '{nome_arquivo}': {e}")
                conn.rollback()

        cursor.close()
        conn.close()
        print("\n--- Conexão com o banco de dados fechada. ---")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("\nERRO DE CONEXÃO: Login failed. Verifique as credenciais no .env e as permissões no SQL Server.")
        else:
            print(f"\nOcorreu um erro de banco de dados: {ex}")
    except Exception as e:
        print(f"\nOcorreu um erro geral: {e}")

if __name__ == "__main__":
    verificar_pastas()
    processar_arquivos_entrada()
    print("\nSimulação de importação de notas concluída.")