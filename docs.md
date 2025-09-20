Omega — Guia de Uso & Contribuição

Bot Discord modular e escalável. Este README explica a arquitetura, como rodar localmente, onde criar novos comandos/funcionalidades, como testar e como contribuir em equipe.

Sumário

Arquitetura

Pré-requisitos

Configuração (.env)

Como rodar

Módulos (Cogs) — onde criar comandos

Serviços — regras de negócio reutilizáveis

Infra — banco de dados e integrações

Tests

Qualidade de código

Estrutura de pastas

Dúvidas comuns

Arquitetura

Camadas principais:

core/: inicialização do bot, logging e settings.

modules/: todos os comandos do Discord (cogs).

services/: regras de negócio independentes do Discord.

infra/: banco de dados, cache, clientes de APIs externas.

utils/: utilitários pequenos (sem regra de negócio).

tests/: testes unitários por módulo/serviço.

Regra de ouro: comando vai em modules/; lógica pesada/reutilizável vai em services/.

Pré-requisitos

Python 3.11+

Token do bot do Discord

(Opcional) MySQL (ex.: Bot-Hosting.net)

Instale dependências:

pip install -r requirements.txt

Configuração (.env)

Crie um arquivo .env na raiz com:

# Discord
OMEGON_TOKEN=seu_token_do_discord

# Database (opcional)
DB_HOST=us.mysql.db.bot-hosting.net
DB_PORT=3306
DB_USER=u483539_IVFUQqVTUC
DB_PASS=coloque_a_senha_aqui
DB_NAME=s483539_omega_db


O carregamento é feito por core.settings.Env.load().

Como rodar

Desenvolvimento:

python -m omega.main


Logs de inicialização:

core/bot.py cria o bot e carrega os cogs de modules/.

modules/ contém os comandos (ex.: hello.py, omegon.py).

Módulos (Cogs) — onde criar comandos

Crie um novo arquivo em modules/ (um por tema).
Exemplo: modules/fun.py:

from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dado")
    async def roll_dice(self, ctx, sides: int = 6):
        """Rola um dado com número de lados escolhido."""
        result = random.randint(1, sides)
        await ctx.send(f"🎲 Você tirou {result} em um dado de {sides} lados!")


Registre o cog em core/bot.py:

# core/bot.py (trecho)
from modules.omegon import Omegon
from modules.hello import Hello
from modules.fun import Fun

def create_bot():
    # ... cria bot e intents
    bot.add_cog(Omegon(bot))
    bot.add_cog(Hello(bot))
    bot.add_cog(Fun(bot))
    return bot

Eventos em cogs

Você também pode ouvir eventos do Discord dentro do módulo:

@commands.Cog.listener()
async def on_ready(self):
    print("Bot online!")

Dicas

Um arquivo por domínio/tema (ex.: moderation.py, music.py, admin.py).

Comandos rápidos → direto no cog.

Comandos que chamam lógica pesada → delegue para services/.

Serviços — regras de negócio reutilizáveis

Coloque lógica pura em services/ para ser chamada de vários comandos.

Exemplo: services/test_generator.py:

def generate_test(template: str) -> str:
    return f"# Test gerado automaticamente\n{template}"


Consumindo no módulo:

from discord.ext import commands
from services.test_generator import generate_test

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gen_test")
    async def gen_test(self, ctx, *, template: str):
        result = generate_test(template)
        await ctx.send(f"```python\n{result}\n```")

Infra — banco de dados e integrações

MySQL: use infra/database.py.

Exemplo de uso dentro de um serviço:

# services/user_service.py
from infra.database import get_connection

def get_user_count() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM users;")
            row = cur.fetchone()
            return int(row["total"])


No comando (cog) chame o serviço:

from discord.ext import commands
from services.user_service import get_user_count

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="users")
    async def users(self, ctx):
        total = get_user_count()
        await ctx.send(f"👥 Usuários no banco: {total}")


Nunca abra conexão direta no cog. Deixe isso para services/ → infra/.

Tests

Execute:

pytest -q


Exemplo de teste de comando (sem acessar Discord real):

# tests/test_hello_command.py
import pytest
from modules.hello import Hello

@pytest.mark.asyncio
async def test_hello_command(mocker):
    bot = mocker.Mock()
    cog = Hello(bot)
    ctx = mocker.AsyncMock()
    await cog.hello(ctx)
    ctx.send.assert_called_once_with("Hello! 👋")

Qualidade de código

Recomendado (ajuste no projeto conforme necessário):

Ruff (lint): ruff check .

Black (format): black .

isort (imports): isort .

pre-commit: rodar hooks antes de cada commit.

Estrutura de pastas
omega/
├── core/                 # criação do bot, settings, logger
├── modules/              # COGS: coloque novos comandos aqui
├── services/             # regras de negócio reutilizáveis
├── infra/                # DB e integrações externas
├── utils/                # helpers
├── tests/                # testes unitários
├── docker/               # infra de apoio (ex.: compose)
├── main.py               # entrypoint: python -m omega.main
└── requirements.txt


Arquivos com __init__.py tornam as pastas pacotes Python.

Dúvidas comuns

Onde criar um novo comando?
→ Em modules/ como um Cog (um arquivo por tema).

Preciso mexer no main.py?
→ Não. main.py só chama core.bot.run().

Como registrar meu novo módulo?
→ Importe o Cog e registre em core/bot.py com bot.add_cog(SeuCog(bot)).

Onde coloco acesso a banco de dados?
→ Em infra/ (conexão) e use via services/. O Cog chama o serviço.

Posso ouvir eventos (on_message, on_ready)?
→ Sim, dentro do Cog usando @commands.Cog.listener().