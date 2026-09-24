from typing import Any, cast

import pytest
from aiogram import Dispatcher
from aiogram.types import TelegramObject, User

from aiogram_dialog_i18n.fluentogram import FluentogramMiddleware, constants
from tests.fluentogram.hub import HUB


def user(language_code: str | None) -> User:
    return User(id=1, is_bot=False, first_name="Bob", language_code=language_code)


async def call(middleware: FluentogramMiddleware, data: dict[str, Any]) -> str:
    async def handler(_: TelegramObject, __: dict[str, Any]) -> None: ...

    await middleware(handler, cast("TelegramObject", None), data)
    assert data[constants.HUB_KEY] is HUB
    return data[constants.RUNNER_KEY].get("hello", name="Bob")


async def test_locale_of_the_user():
    assert await call(FluentogramMiddleware(HUB), {"event_from_user": user("ru")}) == "Привет, Bob!"


@pytest.mark.parametrize("data", [{}, {"event_from_user": user(None)}])
async def test_falls_back_to_root_locale(data: dict[str, Any]):
    assert await call(FluentogramMiddleware(HUB), data) == "Hello, Bob!"


DB = {1: "ru"}  # background updates of BgManager have no language_code


class DbMiddleware(FluentogramMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str | None:
        return DB.get(data["event_from_user"].id)


async def test_get_locale_is_overridden():
    assert await call(DbMiddleware(HUB), {"event_from_user": user(None)}) == "Привет, Bob!"


async def test_constants(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(constants, "RUNNER_KEY", "tr")
    monkeypatch.setattr(constants, "HUB_KEY", "hub")
    data: dict[str, Any] = {"event_from_user": user("ru")}

    assert await call(FluentogramMiddleware(HUB), data) == "Привет, Bob!"
    assert set(data) == {"event_from_user", "tr", "hub"}


def test_setup_registers_for_every_update():
    dp = Dispatcher()
    middleware = FluentogramMiddleware(HUB)
    middleware.setup(dp)
    assert middleware in dp.update.outer_middleware
