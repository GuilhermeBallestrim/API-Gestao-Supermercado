# 🛒 API de Gestão de Supermercado

API RESTful para gerenciamento de clientes, produtos e ordens de venda, desenvolvida com **FastAPI** e armazenamento em arquivos **CSV**.

---

## ⚙️ Como rodar

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

```bash
pip install fastapi[standard]
```

### Iniciar o servidor

```bash
fastapi dev app.py
```

A API estará disponível em: `http://127.0.0.1:8000`

---

## 📬 Como testar no Postman

1. Abra o Postman e crie uma nova requisição
2. Selecione o método HTTP desejado (GET, POST, PUT, DELETE)
3. Insira a URL completa, ex: `http://127.0.0.1:8000/clientes`
4. Para POST e PUT, vá em **Body → raw → JSON** e insira o JSON correspondente
5. Clique em **Send**

---

## 📋 Endpoints

### 👤 Clientes

### `GET /clientes`

Retorna todos os clientes cadastrados. Não requer body.

---

### `POST /clientes`

Adiciona um novo cliente.

**Regras:**

- O campo `id` é gerado automaticamente — não deve ser enviado
- O CPF deve ser único (com ou sem formatação, ex: `123.456.789-00` ou `12345678900`)

**Body:**

```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "nascimento": "1990-05-20",
  "cpf": "123.456.789-00"
}
```

---

### `PUT /clientes`

Atualiza os dados de um cliente existente.

**Regras:**

- O campo `id` é obrigatório no body para identificar o registro a ser alterado
- Todos os outros campos também devem ser enviados com os valores desejados
- O CPF deve continuar único entre os clientes

**Body:**

```json
{
  "id": 1,
  "nome": "João",
  "sobrenome": "Souza",
  "nascimento": "1990-05-20",
  "cpf": "123.456.789-00"
}
```

---

### `DELETE /clientes/{id}`

Remove um cliente pelo ID informado na URL.

**Regras:**

- O `id` deve ser um inteiro válido e existente no cadastro

**Exemplo:** `DELETE /clientes/1`

---

### 📦 Produtos

### `GET /produtos`

Retorna todos os produtos cadastrados. Não requer body.

---

### `POST /produtos`

Adiciona um novo produto.

**Regras:**

- O campo `id` é gerado automaticamente — não deve ser enviado
- O campo `quantidade` não pode ser negativo

**Body:**

```json
{
  "nome": "Arroz",
  "fornecedor": "Tio João",
  "quantidade": 100
}
```

---

### `PUT /produtos`

Atualiza os dados de um produto existente.

**Regras:**

- O campo `id` é obrigatório no body para identificar o registro a ser alterado
- Todos os outros campos também devem ser enviados com os valores desejados
- O campo `quantidade` não pode ser negativo

**Body:**

```json
{
  "id": 1,
  "nome": "Arroz Integral",
  "fornecedor": "Tio João",
  "quantidade": 80
}
```

---

### `DELETE /produtos/{id}`

Remove um produto pelo ID informado na URL.

**Regras:**

- O `id` deve ser um inteiro válido e existente no cadastro

**Exemplo:** `DELETE /produtos/1`

---

### 🧾 Ordens de Venda

### `GET /ordens`

Retorna todas as ordens de venda cadastradas. Não requer body.

---

### `POST /ordens`

Cria uma nova ordem de venda.

**Regras:**

- O campo `id` é gerado automaticamente — não deve ser enviado
- O `cliente_id` deve corresponder a um cliente já cadastrado
- O `produto_id` deve corresponder a um produto já cadastrado
- Ambos os IDs devem ser inteiros positivos

**Body:**

```json
{
  "cliente_id": 1,
  "produto_id": 2
}
```

---

### `PUT /ordens`

Atualiza uma ordem de venda existente.

**Regras:**

- O campo `id` é obrigatório no body para identificar o registro a ser alterado
- O `cliente_id` e o `produto_id` devem corresponder a registros existentes
- Ambos os IDs devem ser inteiros positivos

**Body:**

```json
{
  "id": 1,
  "cliente_id": 2,
  "produto_id": 3
}
```

---

### `DELETE /ordens/{id}`

Remove uma ordem de venda pelo ID informado na URL.

**Regras:**

- O `id` deve ser um inteiro válido e existente no cadastro

**Exemplo:** `DELETE /ordens/1`

---

## 🗂️ Arquivos CSV gerados automaticamente

| Arquivo | Campos |
| --- | --- |
| `Clientes.csv` | id, nome, sobrenome, nascimento, cpf |
| `Produtos.csv` | id, nome, fornecedor, quantidade |
| `OrdemDeVendas.csv` | id, cliente_id, produto_id |

> Os arquivos são criados automaticamente na primeira execução caso não existam.
>
