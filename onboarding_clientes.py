import requests
import pyodbc
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- CONFIGURAÇÃO SEGURA ---
API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')

# Nome do seu Quadro e da Lista no Trello
NOME_QUADRO = 'Controle de Processos'
NOME_LISTA_DESTINO = 'Novos Clientes'

# Configuração do Banco de Dados SQL Server (lida do .env)
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

def obter_id_quadro(nome_quadro):
    """Busca o ID de um quadro pelo nome."""
    url = f"https://api.trello.com/1/members/me/boards?key={API_KEY}&token={API_TOKEN}"
    response = requests.get(url)
    response.raise_for_status() # Lança um erro se a requisição falhar
    for board in response.json():
        if board['name'] == nome_quadro:
            print(f"Quadro '{nome_quadro}' encontrado com ID: {board['id']}")
            return board['id']
    raise Exception(f"Quadro com o nome '{nome_quadro}' não encontrado.")

def obter_id_lista(id_quadro, nome_lista):
    """Busca o ID de uma lista dentro de um quadro pelo nome."""
    url = f"https://api.trello.com/1/boards/{id_quadro}/lists?key={API_KEY}&token={API_TOKEN}"
    response = requests.get(url)
    response.raise_for_status()
    for trello_list in response.json():
        if trello_list['name'] == nome_lista:
            print(f"Lista '{nome_lista}' encontrada com ID: {trello_list['id']}")
            return trello_list['id']
    raise Exception(f"Lista com o nome '{nome_lista}' não encontrada no quadro.")

def criar_cartao_trello(id_lista, nome_cliente, cnpj_cliente):
    """Cria um novo cartão no Trello."""
    url = "https://api.trello.com/1/cards"
    params = {
        'key': API_KEY,
        'token': API_TOKEN,
        'idList': id_lista,
        'name': f"Onboarding: {nome_cliente}",
        'desc': f"Iniciar processo de onboarding para o cliente com CNPJ: {cnpj_cliente}"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    print(f"Cartão para '{nome_cliente}' criado com sucesso!")
    return response.json()


def processar_novos_clientes():
    print("Iniciando processo de onboarding de clientes...")

    if not all([API_KEY, API_TOKEN, DB_SERVER, DB_DATABASE, DB_USER, DB_PASSWORD]):
        print("ERRO: Uma ou mais variáveis de ambiente não foram definidas no arquivo .env")
        return

    try:
        id_quadro = obter_id_quadro(NOME_QUADRO)
        id_lista = obter_id_lista(id_quadro, NOME_LISTA_DESTINO)

        print(f"Conectando ao banco de dados '{DB_DATABASE}'...")
        conn = pyodbc.connect(DB_CONN_STR)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT ProcessadoTrello FROM Clientes WHERE 1=0")
        except pyodbc.ProgrammingError:
            print("Coluna 'ProcessadoTrello' não encontrada. Criando...")
            cursor.execute("ALTER TABLE Clientes ADD ProcessadoTrello BIT DEFAULT 0")
            conn.commit()

        cursor.execute("SELECT ClienteID, Nome, CNPJ FROM Clientes WHERE ProcessadoTrello = 0 OR ProcessadoTrello IS NULL")
        novos_clientes = cursor.fetchall()

        if not novos_clientes:
            print("Nenhum novo cliente para processar.")
            return

        print(f"Encontrados {len(novos_clientes)} novos clientes.")

        for cliente in novos_clientes:
            cliente_id, nome, cnpj = cliente
            print(f"\nProcessando cliente: {nome}")
            
            criar_cartao_trello(id_lista, nome, cnpj)

            cursor.execute("UPDATE Clientes SET ProcessadoTrello = 1 WHERE ClienteID = ?", cliente_id)
            print(f"Cliente ID {cliente_id} marcado como processado no banco de dados.")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("\nProcesso concluído com sucesso!")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '28000':
            print("\nERRO DE CONEXÃO: Login failed. Verifique as credenciais no .env e as permissões no SQL Server.")
        else:
            print(f"\nOcorreu um erro de banco de dados: {ex}")
    except Exception as e:
        print(f"\nOcorreu um erro geral: {e}")

if __name__ == "__main__":
    processar_novos_clientes()
