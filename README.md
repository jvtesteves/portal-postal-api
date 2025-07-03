# API de Rastreio - Portal Postal

Esta é uma API criada com FastAPI que utiliza Selenium para realizar web scraping no Portal Postal e obter o status de um pedido a partir do número da nota fiscal.

## Funcionalidades

- **Consulta por Nota Fiscal:** Um endpoint que recebe um número de nota fiscal e retorna o código de rastreio e o último status do pedido.
- **Segurança:** As credenciais de acesso ao portal são carregadas a partir de variáveis de ambiente para maior segurança, não sendo expostas no código-fonte.
- **Documentação Automática:** A API conta com a documentação interativa do FastAPI (Swagger UI).

---

## 🚀 Como Configurar e Executar o Projeto

### 1. Pré-requisitos

- Python 3.8 ou superior
- Git

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO_AQUI>
cd <NOME_DO_DIRETORIO>
```

### 3. Configurar as Variáveis de Ambiente

Este projeto precisa de credenciais para acessar o Portal Postal. Para isso, você deve criar um arquivo `.env`.

1.  Copie o arquivo de exemplo:

    ```bash
    cp .env.example .env
    ```

2.  Abra o arquivo `.env` em um editor de texto e preencha com suas credenciais:

    ```ini
    PORTAL_EMPRESA_ID="SEU_ID_DE_EMPRESA"
    PORTAL_USERNAME="SEU_USUARIO"
    PORTAL_PASSWORD="SUA_SENHA"
    ```

### 4. Instalar as Dependências

Crie um ambiente virtual (recomendado) e instale as bibliotecas necessárias a partir do `requirements.txt`.

```bash
# Crie e ative um ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`

# Instale as dependências
pip install -r requirements.txt
```

### 5. Executar a API

Com as dependências instaladas e o `.env` configurado, inicie o servidor da API com o Uvicorn.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- `--reload`: Faz com que o servidor reinicie automaticamente após alterações no código.

### 6. Acessar a API

A API estará disponível em `http://localhost:8000`.

- **Para testar e ver a documentação interativa**, acesse: `http://localhost:8000/docs`
- **Para fazer uma consulta**, envie uma requisição GET para: `http://localhost:8000/consultar/{numero_da_nota_fiscal}`

---

## 📦 Estrutura do Projeto

```
. 
├── .env.example      # Exemplo de arquivo para variáveis de ambiente
├── .gitignore        # Arquivos e pastas a serem ignorados pelo Git
├── automacao.py      # Contém toda a lógica de web scraping com Selenium
├── main.py           # Ponto de entrada da API FastAPI
├── README.md         # Este arquivo
└── requirements.txt  # Lista de dependências Python do projeto
```
