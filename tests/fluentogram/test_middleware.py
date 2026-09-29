from typing import Any, cast

import pytest
from aiogram.types import TelegramObject, User

from aiogram_dialog_i18n.fluentogram import FluentogramMiddleware
from tests.fluentogram.hub import HUB


def user(language_code: str | None) -> User:
    return User(id=1, is_bot=False, first_name="Bob", language_code=language_code)


async def call(middleware: FluentogramMiddleware, data: dict[str, Any]) -> str:
    async def handler(_: TelegramObject, __: dict[str, Any]) -> None: ...

    await middleware(handler, cast("TelegramObject", None), data)
    assert data[middleware.hub_key] is HUB
    return data[middleware.runner_key].get("hello", name="Bob")


async def test_locale_of_the_user():
    assert await call(FluentogramMiddleware(HUB), {"event_from_user": user("ru")}) == "Привет, Bob!"


@pytest.mark.parametrize("data", [{}, {"event_from_user": user(None)}], ids=["no_user", "no_language_code"])
async def test_without_language_code_is_root_locale(data: dict[str, Any]):
    assert await call(FluentogramMiddleware(HUB), data) == "Hello, Bob!"


async def test_default_keys():
    # handlers take them as arguments: i18n: TranslatorRunner, translator_hub: TranslatorHub
    data: dict[str, Any] = {"event_from_user": user("ru")}
    await call(FluentogramMiddleware(HUB), data)
    assert {"i18n", "translator_hub"} <= set(data)


async def test_keys():
    data: dict[str, Any] = {"event_from_user": user("ru")}
    assert await call(FluentogramMiddleware(HUB, runner_key="tr", hub_key="hub"), data) == "Привет, Bob!"
    assert not {"i18n", "translator_hub"} & set(data)
