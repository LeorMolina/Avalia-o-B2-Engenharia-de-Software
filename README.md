# 🌍 EcoTrack: O Sistema Sustentável

[cite_start]O **EcoTrack** é um sistema desenvolvido em Python com a arquitetura Model-View-Controller (MVC) para monitorar e analisar ações sustentáveis realizadas por colaboradores em empresas[cite: 17, 21]. [cite_start]Criado em resposta ao chamado da OITV (Organização Internacional de Tecnologia Verde) [cite: 20] [cite_start]para combater a poluição digital e a pegada de carbono[cite: 18, 19].

## 🛠️ Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando os seguintes componentes:

* **Linguagem:** Python 3.x
* [cite_start]**Banco de Dados:** MySQL [cite: 6]
* [cite_start]**Acesso a Dados:** `mysql.connector` [cite: 33]
* [cite_start]**Interface Gráfica:** Tkinter (incluso no Python) [cite: 34, 74]
* **Arquitetura:** Model-View-Controller (MVC)

## 📦 Estrutura do Projeto

O sistema é modularizado em quatro arquivos principais seguindo o padrão MVC:

1.  [cite_start]`db_config.py`: Contém a função de conexão com o banco de dados MySQL[cite: 44].
2.  [cite_start]`model.py`: Implementa a classe `AcoesModel`, responsável pela persistência e manipulação dos dados (CRUD)[cite: 57, 60, 63].
3.  [cite_start]`view.py`: Implementa a interface gráfica (`AcoesView`) utilizando Tkinter[cite: 71, 74, 78].
4.  [cite_start]`controller.py`: Implementa a classe `AcoesController`, o elo que conecta as ações da View com a lógica do Model[cite: 89, 93, 95].
5.  [cite_start]`main.py`: O ponto de entrada que instancia as três camadas e inicia a aplicação[cite: 110, 112].

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar o ambiente e executar o EcoTrack.

### 1. Pré-requisitos

* **Python 3.x** instalado.
* **MySQL Server** instalado e rodando.
* [cite_start]Credenciais do MySQL: `user="root"`, `password="Root"` (ajuste no `db_config.py` se necessário)[cite: 49, 50].

### 2. Instalação de Dependências

Instale a biblioteca `mysql-connector-python`:

```bash
pip install mysql-connector-python