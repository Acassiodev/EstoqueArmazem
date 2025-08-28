from fastapi import FastAPI
from app.database import engine
from app.models import category_model, product_model, stock_movement_model
from app.routers import category_router, product_router # você vai criar o product_router

# Cria todas as tabelas no banco de dados (na primeira execução)
category_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
stock_movement_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Estoque",
    description="API RESTful para controle de categorias, produtos e movimentações de estoque.",
    version="1.0.0"
)

# Inclui os routers na aplicação principal
app.include_router(category_router.router)
# app.include_router(product_router.router) # Descomente quando criar

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Estoque!"}

# Em app/main.py

from fastapi import FastAPI
from app.database import engine
from app.models import category_model, product_model, stock_movement_model
# Garanta que a importação está correta
from app.routers import category_router, product_router

# ... (código que cria as tabelas) ...

app = FastAPI(
    # ... (título, descrição, etc.) ...
)

# Inclui os routers na aplicação principal
app.include_router(category_router.router)
app.include_router(product_router.router) # Garanta que esta linha está ativa

# Em app/main.py

import logging
from fastapi import FastAPI
from app.database import engine
from app.models import category_model, product_model, stock_movement_model
from app.routers import category_router, product_router

# -------------------------------------------------------------------
# CONFIGURAÇÃO DO LOGGING - DEVE ESTAR AQUI NO TOPO, APÓS OS IMPORTS
# -------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cria as tabelas no banco de dados, se não existirem
category_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
stock_movement_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Estoque",
    description="API RESTful para controle de categorias, produtos e movimentações de estoque.",
    version="1.0.0"
)

# Inclui os routers na aplicação principal
app.include_router(category_router.router)
app.include_router(product_router.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Estoque!"}