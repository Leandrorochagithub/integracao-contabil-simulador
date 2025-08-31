Simulador de Integração Contábil
Microsserviço de automação em Python que simula um ecossistema de integração de sistemas para um escritório de contabilidade, resolvendo problemas de fluxo de trabalho manual.


<img width="912" height="132" alt="Captura de tela 2025-08-31 092032" src="https://github.com/user-attachments/assets/92cb90e1-5133-43c9-8791-00ce59b33d7f" />


<img width="1211" height="283" alt="Captura de tela 2025-08-31 092130" src="https://github.com/user-attachments/assets/8ecef158-a0b0-4e76-a985-9d31dace1a1d" />


<img width="1005" height="371" alt="Captura de tela 2025-08-31 092210" src="https://github.com/user-attachments/assets/0abd3996-bb8e-45a6-99ad-854a38f22218" />



<img width="1185" height="305" alt="Captura de tela 2025-08-31 100943" src="https://github.com/user-attachments/assets/10b85942-08c8-416a-92fc-2678b55badc8" />

🎯 O Desafio de Negócio
Em muitos escritórios de contabilidade, uma grande parte do trabalho é manual e repetitivo: importar notas fiscais de clientes, cadastrar novos clientes em múltiplos sistemas, criar cronogramas de tarefas e gerar relatórios. Essas tarefas são lentas, consomem horas de trabalho qualificado e são suscetíveis a erros humanos.

Este projeto simula uma solução de automação para resolver esses problemas, criando um fluxo de dados coeso e confiável.

💡 A Solução Proposta

Foi desenvolvido um conjunto de scripts em Python que atuam como um "hub" de integração, simulando um ecossistema real com as seguintes ferramentas:

ERP (Sistema Domínio): Simulado por um banco de dados Microsoft SQL Server.

Captura de Notas (Qvei): Simulada por uma pasta local que é monitorada em busca de novos arquivos .csv.

Gestor de Tarefas (Gclick): Simulado pela API do Trello, onde o onboarding de novos clientes é gerenciado.

Auditoria Fiscal (Fiscontech): Simulada pela geração de relatórios mensais em formato .xlsx.

Arquitetura da Simulação
graph TD
    subgraph "Entrada de Dados"
        A[Pasta de Entrada de Notas .csv]
    end

    subgraph "Processamento (Python)"
        B{Scripts de Automação}
    end

    subgraph "Sistemas de Destino"
        C[Banco de Dados SQL Server]
        D{API do Trello}
        E[Pasta de Saída de Relatórios .xlsx]
    end

    A -- Importação --> B;
    B -- Insere/Atualiza Dados --> C;
    C -- Consulta Novos Clientes --> B;
    B -- Cria Cards de Onboarding --> D;
    B -- Gera Relatórios --> E;

🛠️ Tecnologias Utilizadas
Linguagem: Python 3

Banco de Dados: Microsoft SQL Server

Bibliotecas Python:

pyodbc para conexão com o SQL Server.

pandas para manipulação e processamento de dados em arquivos.

requests para consumo da API REST do Trello.

API Externa: Trello API

Ferramentas: Git, GitHub, Visual Studio Code

🚀 Como Executar o Projeto
Pré-requisitos:

Python 3.x instalado.

Microsoft SQL Server (Developer Edition) instalado e rodando.

Uma conta gratuita no Trello.

Setup do Banco de Dados:

Crie um banco de dados chamado SimuladorERP.

Execute os scripts do arquivo database/schema.sql (disponível neste repositório) para criar as tabelas necessárias.

Configuração do Ambiente:

Instale as dependências: pip install -r requirements.txt

Configure suas credenciais da API do Trello e do banco de dados nos scripts da pasta scripts/.

Executando as Simulações:

Importação de Notas: Coloque um arquivo .csv na pasta de entrada e execute python scripts/importador_notas.py.

Onboarding de Clientes: Insira um novo cliente no banco de dados e execute python scripts/onboarding_clientes.py para ver o card ser criado automaticamente no Trello.

✨ Habilidades Demonstradas
Automação de Processos (ETL): Desenvolvimento de scripts para extrair, transformar e carregar dados entre diferentes fontes (arquivos, banco de dados).

Integração com APIs REST: Consumo de serviços externos (Trello) para automação de workflows e processos de negócio.

Gerenciamento de Banco de Dados: Modelagem de schema, criação de tabelas e manipulação de dados com SQL (T-SQL).

Desenvolvimento em Python: Uso de bibliotecas padrão do mercado (pandas, requests) para construir soluções robustas e resolver problemas reais.
