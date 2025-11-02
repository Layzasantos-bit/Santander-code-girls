# 🚀 Desafio DIO: Tarefas Automatizadas com AWS Lambda e S3

Este repositório documenta a implementação do laboratório "Consolidando conhecimentos em tarefas automatizadas com Lambda Function e S3" da [Digital Innovation One (DIO)](https://dio.me/).

O objetivo foi aplicar os conceitos de arquitetura serverless e event-driven (orientada a eventos) para criar um fluxo de automação. O projeto implementa o padrão "S3-Lambda-DynamoDB", onde o upload de um arquivo em um bucket S3 dispara uma função Lambda que processa o arquivo e registra seus metadados em uma tabela do DynamoDB.

## 📌 Sumário

* [Arquitetura do Projeto](#-arquitetura-do-projeto)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Conceitos-Chave Aplicados](#-conceitos-chave-aplicados)
* [Infraestrutura como Código (IaC)](#-infraestrutura-como-código-iac)
* [Resultados e Insights](#-resultados-e-insights)
* [Conclusão](#-conclusão)

## 🏛️ Arquitetura do Projeto

A solução implementada é baseada no "Estudo de Caso" apresentado nas aulas, focando no fluxo assíncrono de processamento de arquivos.

O fluxo de dados é o seguinte:

1.  **Upload do Usuário:** Um usuário ou sistema externo faz o upload de um novo arquivo (ex: `relatorio.csv`) no **Amazon S3 Bucket** (`dio-desafio-s3-lambda-uploads`).
2.  **Disparo do Evento (Trigger):** O S3 detecta o evento `s3:ObjectCreated:*` e automaticamente invoca a **Função AWS Lambda** (`dio-desafio-s3-processor`).
3.  **Processamento da Lambda:**
    * A função recebe o evento contendo os detalhes do bucket e do arquivo (`key`).
    * Ela usa o cliente S3 para buscar os metadados do objeto (como `ContentLength`, `ContentType`, `ETag`).
    * Ela gera um ID único (`uuid`) e um timestamp.
4.  **Registro no Banco:** A Lambda formata esses dados e os insere como um novo item na tabela do **Amazon DynamoDB** (`dio-desafio-registros-arquivos`), criando um catálogo de todos os arquivos processados.

## 🛠️ Tecnologias Utilizadas

* **Amazon S3:** Usado como repositório de objetos e como fonte de eventos para o workflow.
* **AWS Lambda:** O cérebro da operação (computação serverless). Executa a lógica de negócios para processar o arquivo e salvar no banco.
* **Amazon DynamoDB:** Banco de dados NoSQL serverless usado para persistir os metadados dos arquivos processados.
* **AWS IAM (Identity and Access Management):** Para gerenciar as permissões (Execution Role) que a Lambda precisa para ler do S3 e escrever no DynamoDB.
* **AWS SAM / CloudFormation:** Utilizado para definir toda a infraestrutura como código (IaC) no arquivo `template.yaml`.

## 🧠 Conceitos-Chave Aplicados

* **Arquitetura Orientada a Eventos (Event-Driven):** O workflow é reativo. A computação só é acionada quando um evento (upload no S3) ocorre.
* **Serverless:** Toda a arquitetura é baseada em serviços gerenciados, sem a necessidade de provisionar ou gerenciar servidores (S3, Lambda, DynamoDB).
* **S3 Event Notifications:** Configuração do S3 para atuar como um *producer* de eventos, disparando a função Lambda.
* **Desacoplamento:** O serviço que faz o upload no S3 não precisa saber que existe uma função Lambda ou um banco de dados. Os componentes são independentes.
* **Infraestrutura como Código (IaC):** O uso do `template.yaml` (AWS SAM) permite que toda a arquitetura seja criada, atualizada e excluída de forma automatizada e replicável.

## 📑 Infraestrutura como Código (IaC)

O arquivo [template.yaml](template.yaml) neste repositório define todos os recursos e permissões necessários usando o AWS Serverless Application Model (SAM):

1.  **`AWS::S3::Bucket` (`UploadBucket`):** O bucket de origem.
2.  **`AWS::DynamoDB::Table` (`RegistrosTable`):** A tabela de destino com uma chave primária `id`.
3.  **`AWS::Serverless::Function` (`S3ProcessFunction`):**
    * Define a função Lambda, apontando para o código em `src/app.py`.
    * **`Policies`:** Concede as permissões necessárias (`S3ReadPolicy`, `DynamoDBCrudPolicy`).
    * **`Events`:** Configura o gatilho, conectando o evento `s3:ObjectCreated:*` do `UploadBucket` a esta função.

O código da função Lambda se encontra em [src/app.py](src/app.py).

## ✨ Resultados e Insights

* **Velocidade de Implementação:** O padrão S3-Lambda-DynamoDB é um dos mais comuns e poderosos da AWS. Usando IaC (SAM), é possível implantar todo o fluxo em minutos.
* **Escalabilidade Automática:** Esta arquitetura lida com 1 ou 1 milhão de arquivos por dia sem qualquer alteração de configuração, pois S3, Lambda e DynamoDB escalam automaticamente.
* **Depuração (Debugging):** O monitoramento é feito via Amazon CloudWatch Logs, onde cada `print()` da função Lambda é registrado, facilitando a identificação de erros no processamento.

