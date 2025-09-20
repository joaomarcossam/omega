# Omega — Guia rápido da arquitetura (copiar e colar)

> **Pra que serve:** dizer **onde** colocar cada coisa e **como** usar os blocos.  
> Sem passos de instalação.

---

## Camadas (o que vai em cada pasta)

- **`core/`**  
  Bootstrap do bot. Cria o `commands.Bot`, carrega cogs de `modules/`, configura `settings` e `logger`.
  - `bot.py`: cria e registra cogs.
  - `settings.py`: carrega env/config.
  - `logger.py`: logging central.

- **`modules/`**  
  **Todos os comandos e eventos** do Discord (Cogs).
  - Um arquivo por domínio/tema (ex.: `hello.py`, `admin.py`, `fun.py`).
  - Pode ter listeners (`on_ready`, `on_message`) dentro do Cog.

- **`services/`**  
  **Regra de negócio reutilizável** (não importa `discord.*`).  
  - Lógica pesada/compartilhada entre cogs.

- **`infra/`**  
  **I/O**: banco de dados, APIs externas, cache.  
  - Conexões/clients e funções de acesso.

- **`utils/`**  
  Helpers pequenos (formatadores, conversões). **Sem regra de negócio**.

- **`tests/`**  
  Testes por módulo/serviço. Cogs testam comportamento com serviços mockados.

> **Regra de ouro:** Cog **não** fala com DB/API direto. Cog → Service → Infra.

---

## Fluxo

1) `main.py` chama `core.bot.run()`  
2) `core/bot.py` cria o Bot e **registra** cogs de `modules/`  
3) Cog recebe comando/evento do Discord  
4) Cog chama função em `services/` (regra de negócio)  
5) `services/` usa `infra/` (DB/APIs) quando precisar

---

## Árvore de referência

omega/
├─ core/
│  ├─ bot.py           # cria o bot e registra cogs
│  ├─ settings.py      # carrega configs/env
│  └─ logger.py        # configura logging
├─ modules/
│  ├─ omegon.py        # cog com comandos/eventos
│  └─ hello.py         # cog de exemplo
├─ services/
│  └─ test_generator.py
├─ infra/
│  ├─ database.py
│  └─ external_api.py
├─ utils/
│  ├─ font.py
│  └─ message.py
└─ tests/
   └─ test_hello_command.py



---

## Fluxo

1. `main.py` chama `core.bot.run()`.
2. `core/bot.py` cria o `Bot` e registra cogs de `modules/`.
3. Um **Cog** em `modules/` recebe o input do Discord (comandos/eventos).
4. O Cog chama **services/** (regra de negócio).
5. **services/** usa **infra/** (DB/APIs).

> **Regra:** Cog **não** acessa DB nem APIs direto. Cog → Service → Infra.

---

## Novo comando (Cog)

**Arquivo:** `modules/novo_modulo.py`
```py
from discord.ext import commands
from services.meu_servico import faz_algo

class NovoModulo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="acao")
    async def acao(self, ctx, *, arg: str):
        resultado = faz_algo(arg)
        await ctx.send(resultado)
        
```

---

## Registro no bot (core/bot.py)

**Arquivo:** `core/bot.py`
```py
from modules.novo_modulo import NovoModulo

def create_bot():
    # ... criar intents e bot = commands.Bot(...)
    bot.add_cog(NovoModulo(bot))
    return bot
    
```

## Novo evento (listener) no Cog


from discord.ext import commands
```py
class MeuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # logs, métricas, preload, etc.
        ...
```

Eventos pertencem ao cog responsável pelo domínio daquela lógica.

## Nova funcionalidade com regra de negócio

Service: services/minha_regra.py

```py
from infra.database import get_connection

def lista_usuarios():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users")
            return cur.fetchall()

```

Cog: modules/admin.py

```py
from discord.ext import commands
from services.minha_regra import lista_usuarios

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="usuarios")
    async def usuarios(self, ctx):
        rows = lista_usuarios()
        nomes = ", ".join([r["name"] for r in rows])
        await ctx.send(f"👥 {nomes or 'Sem usuários'}")
```

## Import padrão (pacote raiz)

```py
from omega.modules.hello import Hello
from omega.services.test_generator import generate_test
from omega.infra.database import get_connection
```

Rode via python -m omega.main para manter imports a partir de omega.*.

## Diretrizes de testes

Cogs: teste comandos com ctx mockado; não bater em DB/API real.

Services: teste lógica pura; mock de infra.

Infra: testes de integração isolados (se necessário).

Exemplo mínimo (Cog)

```py
import pytest
from modules.hello import Hello

@pytest.mark.asyncio
async def test_hello(mocker):
    cog = Hello(mocker.Mock())
    ctx = mocker.AsyncMock()
    await cog.hello(ctx)
    ctx.send.assert_called_once()
```

## Convenções

Cogs: sem SQL, sem requests diretos.

Services: sem import discord.*.

Infra: sem regra de negócio.

Utils: funções puras/reutilizáveis, sem side effects relevantes.

Imports: usar omega.* como raiz.

Registro de cogs: centralizado em core/bot.py.

## Escala

Novos cogs: adicionar arquivo em modules/ e registrar em core/bot.py.

Feature flags: carregar cogs condicionalmente conforme config/env.

Sharding/múltiplas instâncias: manter criação do Bot centralizada em core/.

## Checklist PR

 Comando novo está em modules/ (Cog).

 Lógica pesada em services/.

 Acesso a DB/APIs só em infra/.

 Imports a partir de omega.*.

 Testes mínimos do que foi criado.