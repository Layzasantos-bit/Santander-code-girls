# 🚀 Desafio DIO: Infraestrutura Automatizada com AWS CloudFormation

Este repositório documenta o projeto final do desafio "Implementar uma infraestrutura automatizada com AWS CloudFormation" da [Digital Innovation One (DIO)](https://dio.me/).

O objetivo foi aplicar os conceitos de **Infraestrutura como Código (IaC)** para provisionar de forma declarativa e automatizada um ambiente de rede fundamental na AWS: uma **Virtual Private Cloud (VPC)** customizada.

## 📌 Sumário

* [Infraestrutura como Código (IaC) e CloudFormation](#-infraestrutura-como-código-iac-e-cloudformation)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Conceitos-Chave Aplicados](#-conceitos-chave-aplicados)
* [Descrição do Template (`vpc-stack.yaml`)](#-descrição-do-template-vpc-stackyaml)
* [Resultados e Insights](#-resultados-e-insights)
* [Conclusão](#-conclusão)

## 💡 Infraestrutura como Código (IaC) e CloudFormation

**Infraestrutura como Código (IaC)** é a prática de gerenciar e provisionar infraestrutura de TI por meio de arquivos de definição legíveis por máquina (código), em vez de processos manuais ou ferramentas interativas.

O **AWS CloudFormation** é o serviço nativo da AWS para IaC. Ele permite que usemos um arquivo **template** (escrito em YAML ou JSON) para modelar e provisionar todos os recursos da AWS em nossa nuvem. O CloudFormation interpreta esse template e cuida de criar, configurar e conectar os recursos na ordem correta, gerenciando todas as dependências.

Isso nos permite tratar nossa infraestrutura como software: ela pode ser versionada, revisada, reutilizada e auditada, garantindo consistência e eliminando desvios de configuração.

## 🛠️ Tecnologias Utilizadas

* **AWS CloudFormation:** Serviço de orquestração de IaC.
* **AWS VPC (Virtual Private Cloud):** Para criar a rede privada isolada.
* **AWS EC2 (Recursos de Rede):** Subnets, Route Tables, Internet Gateways.
* **YAML:** Linguagem de marcação usada para escrever o template.

## 🧠 Conceitos-Chave Aplicados

Durante o laboratório, os seguintes conceitos fundamentais do CloudFormation foram aplicados:

* **Templates:** O arquivo YAML (`vpc-stack.yaml`) que serve como a "planta baixa" da nossa infraestrutura.
* **Stacks:** A unidade de implantação do CloudFormation. É a instância de um template, ou seja, o conjunto de recursos reais criados.
* **Parameters:** Permitem que o template seja reutilizável, solicitando entradas no momento da criação da stack (ex: `VPCCidrBlock`, `AvailabilityZone`).
* **Resources:** A seção principal do template, onde declaramos os recursos que a AWS deve criar (ex: `AWS::EC2::VPC`, `AWS::EC2::Subnet`).
* **Funções Intrínsecas (`!Ref`, `!GetAtt`):**
    * `!Ref`: Usada para referenciar o valor de um Parâmetro (ex: `!Ref VPCCidrBlock`) ou o ID de outro Recurso (ex: `!Ref VPC`).
    * `DependsOn`: Usado para definir dependências explícitas, garantindo que um recurso (como a Rota) só seja criado após outro (como o GatewayAttachment).
* **Outputs:** Permitem que a Stack exponha informações úteis (como o ID da VPC) para serem usadas por outras stacks ou para consulta.

## 🔧 Descrição do Template (`vpc-stack.yaml`)

O template [vpc-stack.yaml](vpc-stack.yaml) provisiona uma arquitetura de rede básica, porém fundamental, consistindo em:

1.  **Uma VPC (`AWS::EC2::VPC`):**
    * Cria a rede isolada com um bloco CIDR definido por parâmetro (padrão `10.0.0.0/16`).

2.  **Um Internet Gateway (`AWS::EC2::InternetGateway`):**
    * O componente que permite a comunicação da VPC com a internet.

3.  **Um Gateway Attachment (`AWS::EC2::VPCGatewayAttachment`):**
    * "Conecta" o Internet Gateway à VPC.

4.  **Uma Subnet Pública (`AWS::EC2::Subnet`):**
    * Uma sub-rede dentro da VPC (padrão `10.0.1.0/24`) que terá acesso à internet.

5.  **Uma Tabela de Rotas (`AWS::EC2::RouteTable`):**
    * A "lista de regras" de tráfego de rede.

6.  **Uma Rota Padrão (`AWS::EC2::Route`):**
    * Adiciona uma rota à Tabela de Rotas, direcionando todo o tráfego de saída (`0.0.0.0/0`) para o Internet Gateway.

7.  **Uma Associação de Tabela de Rotas (`AWS::EC2::SubnetRouteTableAssociation`):**
    * "Anexa" a Tabela de Rotas à nossa Subnet Pública, efetivamente tornando-a pública.

## ✨ Resultados e Insights

* **Gerenciamento de Dependências:** O maior insight foi observar como o CloudFormation gerencia automaticamente a ordem de criação. Ele entende que não pode anexar um Internet Gateway (IGW) a uma VPC antes que a VPC exista. A cláusula `DependsOn` foi usada para forçar a ordem onde a referência implícita não era suficiente.
* **Reprodutibilidade:** O mesmo template pode ser usado para criar ambientes idênticos (ex: Dev, QA, Prod) simplesmente mudando os parâmetros, garantindo consistência total.
* **Clean-up (Limpeza):** A maior vantagem operacional. Ao excluir a Stack, o CloudFormation remove *todos* os recursos que ele criou, na ordem inversa correta. Isso evita "lixo" de recursos órfãos na conta e custos inesperados.

### Imagens da Execução

**1. Stack Criada com Sucesso (`CREATE_COMPLETE`)**

![Stack Criada com Sucesso](images/stack-create-complete.png)

**2. Recursos Criados (Console da VPC)**

![Recursos Criados no Console da VPC](images/vpc-resources-created.png)

## 🏁 Conclusão

Este laboratório foi fundamental para solidificar os conceitos de Infraestrutura como Código. O AWS CloudFormation é uma ferramenta poderosa que traz os princípios de engenharia de software (versionamento, revisão, automação) para o gerenciamento de infraestrutura, sendo essencial para criar ambientes de nuvem robustos, escaláveis e consistentes.
