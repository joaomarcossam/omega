import pytest
from modules.hello import Hello

@pytest.mark.asyncio
async def test_hello_command(mocker):
    bot = mocker.Mock()
    cog = Hello(bot)
    ctx = mocker.Mock()
    await cog.hello(ctx)
    ctx.send.assert_called_once_with("Hello! 👋")
