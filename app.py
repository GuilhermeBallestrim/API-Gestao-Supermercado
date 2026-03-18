import csv
import os
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from typing import Optional

app = FastAPI()

# =============================== MODELOS =====================================

class Clientes(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    nascimento: date
    cpf: str

class Produtos(BaseModel):
    id: Optional[int] = None
    nome: str
    fornecedor: str
    quantidade: int

class OrdemDeVendas(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    produto_id: int

# =============================== GERENCIADOR CSV ==============================

class GerenciadorCSV:
    def __init__(self, nome_arquivo, colunas):
        self.arquivo = nome_arquivo
        self.colunas = colunas
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.colunas)
                writer.writeheader()

    def ler(self):
        with open(self.arquivo, mode='r', encoding='utf-8') as file:
            return list(csv.DictReader(file))

    def salvar_todos(self, lista_dados):
        with open(self.arquivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.colunas)
            writer.writeheader()
            writer.writerows(lista_dados)

# =============================== INSTÂNCIAS ==================================

arquivo_clientes = GerenciadorCSV("Clientes.csv", ["id", "nome", "sobrenome", "nascimento", "cpf"])
arquivo_produtos = GerenciadorCSV("Produtos.csv", ["id", "nome", "fornecedor", "quantidade"])
arquivo_vendas   = GerenciadorCSV("OrdemDeVendas.csv", ["id", "cliente_id", "produto_id"])

# =============================== UTILITÁRIOS =================================

def gerar_novo_id(dados: list) -> int:
    return max([int(d['id']) for d in dados]) + 1 if dados else 1

def normalizar_cpf(cpf: str) -> str:
    return cpf.replace(".", "").replace("-", "")

def cpf_ja_cadastrado(dados: list, cpf_normalizado: str) -> bool:
    return any(normalizar_cpf(i['cpf']) == cpf_normalizado for i in dados)

def id_existe(dados: list, id: int) -> bool:
    return any(int(d['id']) == id for d in dados)

def ids_sao_positivos(*ids: int) -> bool:
    return all(i > 0 for i in ids)

# =================================== CLIENTES ================================

@app.get("/clientes")
def listar_clientes():
    return arquivo_clientes.ler()

@app.post("/clientes")
async def add_cliente(cliente: Clientes):
    dados = arquivo_clientes.ler()
    cpf_normalizado = normalizar_cpf(cliente.cpf)

    if cpf_ja_cadastrado(dados, cpf_normalizado):
        return {"ERRO": "CPF já cadastrado"}

    novo_obj = cliente.model_dump()
    novo_obj['id'] = gerar_novo_id(dados)
    novo_obj['cpf'] = cpf_normalizado
    novo_obj['nascimento'] = novo_obj['nascimento'].isoformat()

    dados.append(novo_obj)
    arquivo_clientes.salvar_todos(dados)
    return {"SUCESSO": "Cliente Adicionado"}

@app.put("/clientes")
async def edit_cliente(cliente: Clientes):
    if cliente.id is None:
        return {"ERRO": "ID é obrigatório para atualização"}

    dados = arquivo_clientes.ler()
    cpf_normalizado = normalizar_cpf(cliente.cpf)

    for item in dados:
        if int(item['id']) == cliente.id:
            item['nome'] = cliente.nome
            item['sobrenome'] = cliente.sobrenome
            item['nascimento'] = cliente.nascimento.isoformat()
            item['cpf'] = cpf_normalizado
            arquivo_clientes.salvar_todos(dados)
            return {"SUCESSO": "Cliente Editado"}

    return {"ERRO": "ID não localizado"}

@app.delete("/clientes/{cliente_id}")
def del_cliente(cliente_id: int):
    dados = arquivo_clientes.ler()
    nova_lista = [d for d in dados if int(d['id']) != cliente_id]

    if len(nova_lista) == len(dados):
        return {"ERRO": "ID não localizado"}

    arquivo_clientes.salvar_todos(nova_lista)
    return {"SUCESSO": "Cliente Removido"}

# =================================== PRODUTOS ================================

@app.get("/produtos")
def listar_produtos():
    return arquivo_produtos.ler()

@app.post("/produtos")
async def add_produto(produto: Produtos):
    if produto.quantidade < 0:
        return {"ERRO": "Quantidade não pode ser negativa"}

    dados = arquivo_produtos.ler()

    novo_obj = produto.model_dump()
    novo_obj['id'] = gerar_novo_id(dados)

    dados.append(novo_obj)
    arquivo_produtos.salvar_todos(dados)
    return {"SUCESSO": "Produto Adicionado"}

@app.put("/produtos")
async def edit_produto(produto: Produtos):
    if produto.id is None:
        return {"ERRO": "ID é obrigatório para atualização"}

    if produto.quantidade < 0:
        return {"ERRO": "Quantidade não pode ser negativa"}

    dados = arquivo_produtos.ler()

    for item in dados:
        if int(item['id']) == produto.id:
            item['nome'] = produto.nome
            item['fornecedor'] = produto.fornecedor
            item['quantidade'] = produto.quantidade
            arquivo_produtos.salvar_todos(dados)
            return {"SUCESSO": "Produto Editado"}

    return {"ERRO": "ID não localizado"}

@app.delete("/produtos/{produto_id}")
def del_produto(produto_id: int):
    dados = arquivo_produtos.ler()
    nova_lista = [d for d in dados if int(d['id']) != produto_id]

    if len(nova_lista) == len(dados):
        return {"ERRO": "ID não localizado"}

    arquivo_produtos.salvar_todos(nova_lista)
    return {"SUCESSO": "Produto Removido"}

# ================================= ORDENS DE VENDA ===========================

@app.get("/ordens")
def listar_ordens():
    return arquivo_vendas.ler()

@app.post("/ordens")
async def add_ordem(ordem: OrdemDeVendas):
    if not ids_sao_positivos(ordem.cliente_id, ordem.produto_id):
        return {"ERRO": "IDs de cliente e produto devem ser positivos"}

    ids_clientes = [int(c['id']) for c in arquivo_clientes.ler()]
    ids_produtos  = [int(p['id']) for p in arquivo_produtos.ler()]

    if ordem.cliente_id not in ids_clientes:
        return {"ERRO": "Cliente não encontrado"}
    if ordem.produto_id not in ids_produtos:
        return {"ERRO": "Produto não encontrado"}

    dados = arquivo_vendas.ler()

    novo_obj = ordem.model_dump()
    novo_obj['id'] = gerar_novo_id(dados)

    dados.append(novo_obj)
    arquivo_vendas.salvar_todos(dados)
    return {"SUCESSO": "Registro de Venda Criado"}

@app.put("/ordens")
async def edit_ordem(ordem: OrdemDeVendas):
    if ordem.id is None:
        return {"ERRO": "ID é obrigatório para atualização"}

    if not ids_sao_positivos(ordem.cliente_id, ordem.produto_id):
        return {"ERRO": "IDs de cliente e produto devem ser positivos"}

    dados = arquivo_vendas.ler()

    for item in dados:
        if int(item['id']) == ordem.id:
            item['cliente_id'] = ordem.cliente_id
            item['produto_id'] = ordem.produto_id
            arquivo_vendas.salvar_todos(dados)
            return {"SUCESSO": "Registro de Venda Editado"}

    return {"ERRO": "ID não localizado"}

@app.delete("/ordens/{ordem_id}")
def del_ordem(ordem_id: int):
    dados = arquivo_vendas.ler()
    nova_lista = [d for d in dados if int(d['id']) != ordem_id]

    if len(nova_lista) == len(dados):
        return {"ERRO": "ID não localizado"}

    arquivo_vendas.salvar_todos(nova_lista)
    return {"SUCESSO": "Registro de Venda Removido"}
