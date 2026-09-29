import pytest
from aiogram_dialog.test_tools import BotClient
from aiogram_dialog.tools.preview import render_preview_content

from tests.aiogram_i18n.library import LIBRARY as AIOGRAM_I18N
from tests.dialog import EN, RU, App
from tests.fluentogram.library import LIBRARY as FLUENTOGRAM


@pytest.fixture(params=[AIOGRAM_I18N, FLUENTOGRAM], ids=["aiogram_i18n", "fluentogram"])
async def app(request: pytest.FixtureRequest) -> App:
    app = App(request.param)
    await app.client.send("/start")
    assert app.shown() == EN
    return app


async def test_locale_is_read_once_per_update(app: App):
    assert app.db.reads == app.reads_per_update


async def test_locale_changed_in_handler_is_shown(app: App):
    await app.click("Hello, RU!")  # found by the translation
    assert app.shown() == RU
    assert app.db.reads == 2 * app.reads_per_update


async def test_bg_update_reads_locale_again(app: App):
    app.db[1] = "ru"  # changed outside of an update, example: in a background task
    await app.bg_update()
    assert app.shown() == RU
    assert app.db.reads == 2 * app.reads_per_update


async def test_fg_reads_locale_again(app: App):
    app.db[1] = "ru"
    await app.fg_show()
    assert app.shown() == RU
    assert app.db.reads == 2 * app.reads_per_update


async def test_every_user_sees_own_locale(app: App):
    app.db[2] = "ru"
    await BotClient(app.dp, user_id=2, chat_id=2).send("/start")
    assert app.shown() == RU
    await app.client.send("redraw")
    assert app.shown() == EN


async def test_preview_shows_key_and_params(app: App):
    # render_preview has no middleware data, the key is shown instead of a translation
    html = await render_preview_content(app.dialog)
    assert "hello(name=Bob)" in html
    assert "hello(name=RU)" in html
