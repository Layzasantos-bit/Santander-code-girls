# Desafio de Arquitetura: Provisionando Instâncias EC2 na AWS

Repositório criado para documentar a conclusão do Desafio de Projeto de arquitetura do bootcamp
## 📝 Descrição do Projeto

Este projeto consiste na documentação prática dos conhecimentos adquiridos no curso de gerenciamento de instâncias **EC2 (Elastic Compute Cloud)** na **Amazon Web Services (AWS)**. O objetivo é registrar o processo de criação de uma arquitetura de nuvem simples, demonstrando a aplicação dos conceitos de rede, segurança e provisionamento de máquinas virtuais.

---

### ✔️ Status do Projeto

**Projeto Concluído**

---

### 🏗️ Arquitetura e Funcionalidades
1)projeto 2
Uma pipeline que transsforma arquivos de várias fontes em arquivo sql que é descarregado no banco postgreSQL criado na EC2, depois disso os dados são enviados para um datawarehouse para analise do dados que podem ser apresentados no PowerBI. Todo o processo é orquestrado pelo apache airflow que está no EC2.

2)projeto 1
O diagrama mostra como funciona a solução na AWS. O usuário envia um arquivo pela aplicação, que é armazenado em um volume de entrada (D-EBS). A instância EC2 processa esse arquivo, consulta ou grava informações no banco de dados RDS e salva o resultado em um volume de saída (E-EBS). Assim, o fluxo garante que os dados enviados sejam processados e os resultados fiquem disponíveis para o usuário.

