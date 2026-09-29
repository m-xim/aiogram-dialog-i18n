from typing import Any

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Update
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from aiogram_dialog_i18n.fluentogram import BaseLocaleManager, FluentogramMiddleware, T
from tests.dialog import Library
from tests.fluentogram.hub import HUB


class DbLocaleManager(BaseLocaleManager):
    async def get_locale(self, event: Update, data: dict[str, Any]) -> str | None:
        assert isinstance(event, Update)  # the same before the handler and on render
        return data["db"][data["event_from_user"].id]


def setup(dp: Dispatcher) -> None:
    FluentogramMiddleware(HUB, DbLocaleManager()).setup(dp)


async def pick_ru(callback: CallbackQuery, _: Button, manager: DialogManager) -> None:
    manager.middleware_data["db"][callback.from_user.id] = "ru"  # saved, i18n is not touched


LIBRARY = Library(T, setup, pick_ru, reads_per_update=2)
