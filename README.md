# plus_db_agent

## Descrição
O plus_db_agent é um módulo que facilita a interação com o banco de dados, fornecendo uma interface simples e eficiente para manipulação de dados. Ele é projetado para ser utilizado como uma dependência em outros projetos, proporcionando funcionalidades robustas para operações de banco de dados.

## Funcionalidades
- Conexão e manipulação de bancos de dados.
- Suporte para múltiplos bancos de dados.
- Integração fácil com outros projetos.
- APIs para operações comuns de banco de dados.

## Requisitos
- Python 3.8+
- tortoise-orm 0.21.2

## Instalação
Para usar o plus_db_agent como uma dependência em seu projeto, você pode adicioná-lo diretamente do repositório GitHub.

### Usando Poetry
Adicione a dependência no seu arquivo pyproject.toml:
```toml
[tool.poetry.dependencies]
python = "^3.8"
plus_db_agent = { git = "https://github.com/pedrogs97/plus_db_agent.git", branch = "main" }
```

Depois, instale as dependências:

```sh
poetry install
```

## Uso
Aqui está um exemplo básico de como utilizar o plus_db_agent:

```python
...
from plus_db_agent.manager import init, close

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for the lifespan of the application."""
    await init()
    yield
    await close()
```
