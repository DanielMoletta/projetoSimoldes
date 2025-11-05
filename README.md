# 🚀 Projeto Simoldes: Automação da Folha de Processos

![Status](https://img.shields.io/badge/Status-Concluído_(Acadêmico)-blue)

Este projeto foi desenvolvido como parte do 5º período do curso de Engenharia de Software, com o objetivo de solucionar um desafio real da empresa Simoldes. A aplicação transforma um processo manual e físico de verificação de "folha de processos" em uma plataforma web dinâmica e automatizada.

## 🎯 O Problema

Anteriormente, a verificação da folha de processos era um procedimento inteiramente manual, sujeito a erros, demorado e de difícil rastreabilidade.

## 💡 A Solução

Foi desenvolvida uma aplicação web utilizando **Django (Python)** que virtualiza esse processo. A plataforma permite o gerenciamento digital das informações, agiliza as consultas e, o mais importante, cria **logs de atividades**, garantindo um histórico e maior controle sobre as operações.

---

## 🛠️ Funcionalidades Principais

* **Digitalização do Processo:** Substitui o preenchimento e verificação manual por uma interface web intuitiva.
* **Geração de Relatórios:** Utiliza a biblioteca `matplotlib` para criar visualizações e relatórios dinâmicos a partir dos dados coletados.
* **Exportação de Dados:** Permite a exportação de informações do processo para arquivos Excel (`.xlsx`) utilizando a biblioteca `openpyxl`.
* **Histórico e Logs:** Registra as principais ações na plataforma, permitindo auditoria e rastreabilidade.

## 💻 Tecnologias Utilizadas

* **Back-End:** Python, Django
* **Front-End:** HTML, CSS, JavaScript
* **Banco de Dados:** SQLite
* **Bibliotecas Python:**
    * `matplotlib`: Para a geração de gráficos e relatórios.
    * `openpyxl`: Para manipulação e exportação de arquivos Excel.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto localmente.

**1. Clonar o Repositório**
```bash
git clone [https://github.com/DanielMoletta/projetoSimoldes.git](https://github.com/DanielMoletta/projetoSimoldes.git)
cd projetoSimoldes

2. (Recomendado) Criar um Ambiente Virtual É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
3. Instalar as Dependências Este comando irá ler o arquivo requirements.txt e instalar automaticamente todas as bibliotecas necessárias (Django, matplotlib, etc.).
```bash
pip install -r requirements.txt
```
4. Aplicar as Migrações do Banco Este comando irá criar o arquivo de banco de dados db.sqlite3 e as tabelas necessárias.
```bash
python manage.py migrate
```
5. Iniciar o Servidor
```bash
python manage.py runserver
```
6. Acessar a Aplicação Abra seu navegador e acesse: http://127.0.0.1:8000/


⚠️ Observação Importante
Conforme descrito na documentação, a aplicação atualmente só exibe informações se o banco de dados (SQLite) já contiver dados. Se o banco de dados estiver vazio, a interface não mostrará resultados, pois ela é projetada para ler e processar os dados existentes.