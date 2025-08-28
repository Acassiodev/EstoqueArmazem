🏗️ API de Gerenciamento de Estoque - Armazém de Construção
Uma API RESTful completa para controle de produtos, categorias e movimentações de estoque em loja de materiais de construção. Desenvolvida com Python e FastAPI, seguindo as melhores práticas de arquitetura de software.


✨ Funcionalidades
✅ Gerenciamento de Categorias: Criar, listar, buscar, atualizar e deletar categorias de materiais

✅ Gerenciamento de Produtos: CRUD completo de produtos com SKU único

✅ Controle de Estoque: Registro de entradas/saídas com prevenção de estoque negativo

✅ Histórico de Movimentações: Rastreamento completo para auditoria

🏛️ Arquitetura
text
[Requisição HTTP] → [🌎 Router] → [⚙️ Service] → [🗄️ Repository] → [💾 Banco de Dados]
Router: Endpoints FastAPI com validação de dados

Service: Lógica de negócio e regras específicas

Repository: Acesso isolado ao banco de dados

🚀 Tecnologias
Ferramenta	Descrição
Python 3.10+	Linguagem principal
FastAPI	Framework web high-performance
SQLAlchemy	ORM para banco de dados
SQLite	Banco de dados em desenvolvimento
Pydantic	Validação de dados
🏁 Instalação Rápida
bash
# Clone o projeto
git clone https://github.com/Acassiodev/EstoqueArmazem.git
cd EstoqueArmazem

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Execute a API
uvicorn app.main:app --reload
🕹️ Como Usar
Acesse a documentação interativa:
👉 http://localhost:8000/docs

📋 Boas Práticas
Respostas JSON padronizadas

Códigos HTTP apropriados para cada scenario

Tratamento de erros claro e informativo

Logging para operações críticas




