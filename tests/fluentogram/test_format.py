from typing import Any, cast

import pytest
from aiogram.types import TelegramObject, User
from aiogram_dialog import DialogManager
from magic_filter import F, MagicFilter

from aiogram_dialog_i18n.fluentogram import FluentogramMiddleware, T
from tests.fakes import FakeManager
from tests.fluentogram.hub import HUB


async def make_manager(middleware: FluentogramMiddleware) -> DialogManager:
    """The data of an update of a user with the locale "ru" after the middleware."""
    data: dict[str, Any] = {
        "event_from_user": User(id=1, is_bot=False, first_name="Bob", language_code="ru"),
        "event_update": None,
    }

    async def handler(_: TelegramObject, __: dict[str, Any]) -> None: ...

    await middleware(handler, cast("TelegramObject", None), data)
    return cast("DialogManager", FakeManager(data))


async def test_none_is_empty():
    # a real Fluent bundle raises on None, the widget passes "" instead
    manager = await make_manager(FluentogramMiddleware(HUB))
    assert await T("hello", name=F["missing"]).render_text({}, manager) == "Привет, !"


@pytest.mark.parametrize("locale", ["en", F["lang"]], ids=["str", "magic_filter"])
async def test_locale_takes_hub_not_user_runner(locale: str | MagicFilter):
    manager = await make_manager(FluentogramMiddleware(HUB))
    assert await T("hello", locale, name="Bob").render_text({"lang": "en"}, manager) == "Hello, Bob!"


async def test_any_keys():
    manager = await make_manager(FluentogramMiddleware(HUB, runner_key="tr", hub_key="hub"))
    assert await T("hello", name="Bob").render_text({}, manager) == "Привет, Bob!"
    assert await T("hello", "en", name="Bob").render_text({}, manager) == "Hello, Bob!"


async def test_without_middleware_raises():
    with pytest.raises(ValueError, match="FluentogramMiddleware not found"):
        await T("hello").render_text({}, cast("DialogManager", FakeManager({})))


async def test_preview_shows_key_and_params_without_middleware():
    manager = cast("DialogManager", FakeManager({}, preview=True))
    assert await T("hello", "en", name=F["n"]).render_text({}, manager) == "hello(name={name})"
