# ChatBot Agenda Inteligente Desenvolvido com AWS Lex

## Objetivo

O objetivo deste projeto é desenvolver um chatbot inteligente para a gestão de compromissos, utilizando AWS Lex. O chatbot permite que os usuários:
- Marquem novos compromissos
- Listem compromissos existentes
- Editem compromissos
- Cancelem compromissos

## Tecnologias Utilizadas

- **Python**: Linguagem de programação usada para o desenvolvimento das funções.
- **AWS Lex**: Serviço de chatbot para processamento de linguagem natural.
- **AWS Polly**: Serviço de conversão de texto em fala.
- **AWS DynamoDB**: Banco de dados NoSQL para armazenamento de dados.
- **AWS S3**: Serviço de armazenamento de objetos para armazenar arquivos e dados.
- **AWS API Gateway**: Serviço para criação, publicação e gerenciamento de APIs.
- **AWS Lambda**: Serviço para executar código em resposta a eventos sem gerenciar servidores.
- **Serverless Framework**: Ferramenta para gerenciamento e implantação de funções Lambda e APIs.
- **Slack**: Plataforma de comunicação usada para interação com o chatbot.
- **Slack API**: API utilizada para integração com o Slack.

## Estrutura dos Arquivos e Pastas

```
sprints-6-7-pb-aws-maio/
│
├── api-tts/
│   ├── handler.py                # Funções para a API de Texto para Fala
│   └── serverless.yml            # Configurações do Serverless Framework
│
├── assets/
│   └── sprints6-7.jpg            # Imagem do projeto
│
├── lex-bot-v1/
│   ├── lambda-backend-lex/
│   │   └── salvar-agendamentos-1b7df9a1-740c-4c2a-aced-e8bf7d7f0be7.zip  # Arquivo zip com funções Lambda
│   └── AgendaInteligente-DRAFT-ZJPR9JLFTO-LexJson.zip   # Arquivo zip com o modelo do bot Lex
│
├── .gitignore                     # Arquivos e pastas a serem ignorados pelo Git
├── package.json                  # Dependências do projeto
└── README.md                     # Este arquivo
```

## Instalação e Execução

### Pré-requisitos

Antes de começar, certifique-se de que você tem as seguintes ferramentas instaladas em sua máquina:

1. **Python 3.x**:
   - **Windows**:
     1. Acesse [Python.org](https://www.python.org/downloads/) e baixe o instalador do Python.
     2. Execute o instalador e selecione a opção "Add Python to PATH" antes de clicar em "Install Now".
   - **macOS**:
     1. Acesse [Python.org](https://www.python.org/downloads/) e baixe o instalador para macOS.
     2. Execute o instalador e siga as instruções na tela.
   - **Linux**:
     ```sh
     sudo apt update
     sudo apt install python3 python3-pip
     ```

2. **AWS CLI**:
   - **Instalação**:
     1. Acesse a [documentação oficial da AWS](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) para obter instruções de instalação.
     2. Para verificar a instalação, execute:
        ```sh
        aws --version
        ```
   - **Configuração**:
     1. Configure o AWS CLI com suas credenciais:
        ```sh
        aws configure
        ```
     2. Você será solicitado a fornecer as seguintes informações:
        ```
        AWS Access Key ID [None]: <SUA_ACCESS_KEY_ID>
        AWS Secret Access Key [None]: <SUA_SECRET_ACCESS_KEY>
        Default region name [None]: <REGIAO_PADRAO> (ex: us-east-1)
        Default output format [None]: <FORMATO_PADRAO> (ex: json)
        ```

3. **Serverless Framework**:
   - **Instalação**:
     ```sh
     npm install -g serverless
     ```

### Passos para Instalação

1. Clone o repositório:
   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd sprints-6-7-pb-aws-maio
   ```

2. Instale as dependências:
   ```sh
   npm install
   ```

3. Configure as variáveis de ambiente conforme necessário.

4. Implemente o projeto na AWS usando o Serverless Framework:
   ```sh
   serverless deploy
   ```

## Como Utilizar

1. **Interagir com o Chatbot**:
   - Acesse o chatbot no Slack e utilize os comandos disponíveis para:
     - **Marcar novos compromissos**: Informe a data, horário e tipo de compromisso.
     - **Listar compromissos**: Solicite uma lista de compromissos agendados.
     - **Editar compromissos**: Forneça o ID do compromisso e as novas informações para atualizá-lo.
     - **Cancelar compromissos**: Informe o ID do compromisso que deseja cancelar.

2. **Testar Funcionalidades**:
   - Utilize o Slack para testar as funcionalidades do chatbot, incluindo agendamento, edição, listagem e cancelamento de compromissos.

## Detalhes do Desenvolvimento

Este projeto foi desenvolvido em equipe, seguindo as diretrizes e especificações fornecidas pelo Programa de Bolsas Compass UOL / AWS - MAIO/2024.

- Utilizamos AWS Lex para desenvolver o chatbot e AWS Polly para conversão de texto em fala.
- Implementamos uma API em Python utilizando Serverless Framework para gerenciar funções Lambda e APIs no API Gateway.
- O código foi estruturado e documentado conforme os requisitos do projeto para garantir clareza e manutenibilidade.

## Dificuldades Encontradas

- **Primeira Experiência com AWS Lex**: Enfrentamos desafios iniciais devido à falta de cursos dedicados ao AWS Lex.
- **Integração com Lambda**: Houve dificuldades na integração do Lex com o AWS Lambda.
- **Aplicação de Conceitos**: Tínhamos dificuldades em aplicar conceitos aprendidos em cursos de Alexa Skill Builder no AWS Lex.

## Desenvolvedores

- **Geraldo Mendes Batista Neto**
- **Rayane da Silva Rodrigues**
- **Ytollo Pereira Alves**
- **Jose Luan Fernandes da Silva**
