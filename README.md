
# 🤖 ChatBot - Agenda Inteligente

A Agenda Inteligente é uma aplicação desenvolvida para auxiliar na gestão de compromissos e tarefas diárias. Utilizando Amazon Lex para processamento de linguagem natural e AWS Lambda para a lógica de backend, o sistema permite que os usuários agendem, editem, listem e cancelem compromissos de forma eficiente e intuitiva.

## 📖 Índice

- [📝 Descrição do projeto](#-chatbot---agenda-inteligente)
- [⚙️ Tecnologias utilizadas](#-tecnologias-utilizadas)
- [🏛️ Arquitetura do projeto](#-arquitetura-do-projeto)
- [💬 Fluxo de conversas](#-fluxo-de-conversas)
- [🧱 Estrutura dos arquivos e pastas](#-estrutura-dos-arquivos-e-pastas)
- [🚀 Instalação e execução](#-instalação-e-execução)
   - [Pré-requisitos](#pré-requisitos)
   - [🔧 Passos para instalação](#-passos-para-instalação)
   - [📖 Como utilizar](#-como-utilizar)
- [🛠️ Detalhes do desenvolvimento](#-detalhes-do-desenvolvimento)
- [🚧 Dificuldades encontradas](#-dificuldades-encontradas)
- [👥 Desenvolvedores](#-desenvolvedores)

## 📝 Descrição do projeto

A Agenda Inteligente visa facilitar o gerenciamento de compromissos diários, permitindo aos usuários interagir de forma natural através do Slack para agendar, editar, listar e cancelar compromissos. Com a integração de diversos serviços da AWS, o sistema oferece uma experiência robusta e escalável.

## ⚙️ Tecnologias utilizadas

- **Python**: Linguagem de programação usada para o desenvolvimento das funções.
- **AWS Lex**: Serviço de chatbot para processamento de linguagem natural e gerenciamento de intents.
- **AWS Polly**: Serviço de conversão de texto em fala.
- **AWS DynamoDB**: Banco de dados NoSQL utilizado para gerenciar compromissos.
- **AWS S3**: Serviço de armazenamento de objetos para armazenar arquivos e dados.
- **AWS API Gateway**: Serviço para criação, publicação e gerenciamento de APIs.
- **AWS Lambda**: Serviço para executar código em resposta a eventos sem gerenciar servidores.
- **Serverless Framework**: Ferramenta para gerenciamento e implantação de funções Lambda e APIs.
- **Slack**: Plataforma de comunicação usada para interação com o chatbot.
- **Slack API**: API utilizada para integração com o Slack.

## 🏛️ Arquitetura do projeto

A arquitetura do projeto foi projetada para garantir uma integração eficaz entre os componentes e serviços da AWS, proporcionando uma solução escalável e robusta para o gerenciamento de compromissos. Abaixo está a visão geral da arquitetura:

1. **Usuário**: Interage com o chatbot através do Slack.
2. **Slack API**: Envia as solicitações dos usuários para o AWS Lex.
3. **AWS Lex**:
   - Processa as intenções e extrai entidades das interações do usuário.
   - Interage com a função Lambda para executar operações como marcação, edição, listagem e cancelamento de compromissos.
4. **AWS Lambda**:
   - A função `lambda_function` processa as requisições do AWS Lex e interage com o DynamoDB.
   - Manipula a lógica de negócios, incluindo armazenamento e recuperação de dados de compromissos.
5. **AWS DynamoDB**:
   - Armazena informações sobre compromissos agendados.
   - Utiliza a chave primária `id` para identificar e gerenciar compromissos.
6. **AWS S3** (Opcional):
   - Armazena arquivos e dados relacionados ao projeto.
7. **AWS API Gateway**:
   - Configura endpoints para interação com a API do projeto.
8. **Serverless Framework**:
   - Gerencia e implanta funções Lambda e APIs.
9. **AWS Polly**:
   - Converte texto em fala para respostas audíveis.

### Diagrama de Arquitetura

O fluxo de dados segue o padrão:
- O usuário envia uma mensagem para o Slack.
- O Slack encaminha a mensagem para o AWS Lex.
- O AWS Lex processa a mensagem e invoca a função Lambda apropriada.
- A função Lambda interage com o DynamoDB para obter ou armazenar dados.
- O Lambda retorna a resposta para o AWS Lex, que é então enviada de volta ao Slack para o usuário.

![diagrama-arq](/assets/diagrama-arq.jpg)

**Descrição do Diagrama**: O diagrama acima mostra como o usuário interage com o Slack, que envia solicitações para o AWS Lex. O Lex processa essas solicitações, chama funções Lambda para manipulação de dados, e interage com o DynamoDB para armazenamento e recuperação de compromissos. Finalmente, o AWS Polly pode ser utilizado para converter texto em fala, criando uma resposta mais interativa para o usuário.

## 💬 Fluxo de conversas

O fluxo de conversas do chatbot foi cuidadosamente estruturado para garantir uma experiência de usuário eficiente e intuitiva. A imagem abaixo representa os principais fluxos de conversas:

![fluxo-de-conversas](/assets/fluxo-de-conversas.jpg)

## 🧱 Estrutura dos arquivos e pastas


```
sprints-6-7-pb-aws-maio/
│
├── api-tts/
│   ├── handler.py                   # Funções para a API de Texto para Fala
│   └── serverless.yml               # Configurações do Serverless Framework
│
├── assets/
│   └── sprints6-7.jpg               # Imagem do projeto
│
├── lambda-agendamentos/
│   └── [Arquivos relacionados às funções Lambda para agendamentos] 
│
├── lex-bot-v1/
│   └── SmartAgenda.zip              # Arquivo zip com o modelo do bot Lex, incluindo as intents e slots configurados
│
├── .gitignore                      # Arquivos e pastas a serem ignorados pelo Git
├── package.json                    # Dependências do projeto
└── README.md                       # Este arquivo
```


## 🚀 Instalação e execução

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
3. **Serverless framework**:
   - **Instalação**:
     ```sh
     npm install -g serverless
    ```
### 🔧 Passos para instalação

1. Clone o repositório:
   ```sh
   git clone <https://github.com/Compass-pb-aws-2024-MAIO-A/sprints-6-7-pb-aws-maio/tree/grupo-6>
   cd sprints-6-7-pb-aws-maio
   ```

2. Instale as dependências:
   ```sh
   npm install
   ```

3. Configure as variáveis de ambiente e o DynamoDB:
   - Crie uma tabela DynamoDB chamada `agendamentos` com a chave primária `id` do tipo String.
   - Configure variáveis de ambiente para conectar o Lambda ao DynamoDB e ao AWS Lex.

4. Implemente o projeto na AWS usando o Serverless Framework:
   ```sh
   serverless deploy
   ```
### 📖 Como utilizar

Siga os passos abaixo para configurar e utilizar o ChatBot Agenda Inteligente.

1. **Interagir com o Chatbot**:
   - Acesse o chatbot no Slack e utilize os comandos disponíveis para:
     - **Marcar novos compromissos**: Informe a data, horário, tipo de compromisso e local.
     - **Listar compromissos**: Solicite uma lista de compromissos agendados, que será exibida com IDs para seleção.
     - **Editar compromissos**: Forneça o ID do compromisso e as novas informações (data

, horário, tipo, ou local) que deseja alterar.
     - **Cancelar compromissos**: Solicite o cancelamento informando o ID do compromisso desejado.

2. **Exemplo de Comandos**:
   - Marcar compromisso: `"Marcar reunião para o dia 15/08/2024 às 10:00 sobre Projeto X na Sala de Reuniões 1."`
   - Listar compromissos: `"Quais são meus compromissos agendados?"`
   - Editar compromisso: `"Editar compromisso com ID 123456. Alterar data para 16/08/2024."`
   - Cancelar compromisso: `"Cancelar compromisso com ID 123456."`

## 🛠️ Detalhes do desenvolvimento

1. **Lógica de Agendamento**:
   - Os compromissos são armazenados na tabela DynamoDB `agendamentos`.
   - Cada compromisso possui um `id` único gerado pela função Lambda.
   - A função Lambda é responsável por todas as operações CRUD nos compromissos.

2. **Inteligência no tratamento de erros**:
   - O chatbot foi configurado para lidar com cenários de erro, como datas passadas ou campos obrigatórios ausentes.
   - Caso o usuário não forneça informações para todos os slots ao editar um compromisso, o bot apenas atualiza os slots preenchidos, mantendo os valores anteriores dos slots não preenchidos.

3. **Validação de data e hora**:
   - A função Lambda inclui verificações para garantir que a data e a hora informadas são futuras e separadas.

### Funções lambda

A função Lambda `lambda_function` é responsável por:

- **Marcar compromissos**: Recebe as informações fornecidas pelo AWS Lex e as armazena no DynamoDB.
- **Editar compromissos**: Atualiza as informações de um compromisso existente no DynamoDB, com base no ID fornecido.
- **Listar compromissos**: Recupera e exibe os compromissos agendados para o usuário.
- **Cancelar compromissos**: Remove o compromisso do DynamoDB, com base no ID fornecido.

## 🚧 Dificuldades encontradas

- **Integração com o AWS Lex**: A configuração inicial do bot para reconhecimento correto das intenções (intents) apresentou desafios devido à complexidade das interações do usuário.
- **Gerenciamento do DynamoDB**: A estruturação do banco de dados NoSQL exigiu atenção especial para garantir que as operações de leitura e gravação fossem realizadas de forma eficiente e com consistência.
- **Respostas do Bot**: Ajustar as respostas do bot para serem naturais e claras demandou várias iterações e testes.

## 👥 Desenvolvedores

- **[Geraldo Mendes](https://github.com/Geraldomendes)**
- **[Luan Fernandes](https://github.com/https-Luan-Fernandes)**
- **[Rayane da Silva](https://github.com/RaVeNsszz)**
- **[Ytollo Pereira](https://github.com/YtalloPereira)**
