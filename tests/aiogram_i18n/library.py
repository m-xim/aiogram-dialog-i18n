from aiogram import Dispatcher
from aiogram.types import CallbackQuery, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentCompileCore
from aiogram_i18n.managers import BaseManager
from fluent_compiler.bundle import FluentBundle

from aiogram_dialog_i18n.aiogram_i18n import T
from tests.dialog import Library


class DbManager(BaseManager):
    async def get_locale(self, event_from_user: User, db: dict[int, str]) -> str:
        return db[event_from_user.id]

    async def set_locale(self, locale: str, event_from_user: User, db: dict[int, str]) -> None:
        db[event_from_user.id] = locale


def setup(dp: Dispatcher) -> None:
    core = FluentCompileCore(path="unused")
    # locales are set here, BotClient does not run dp.startup that loads them from files
    core.locales = {
        "en": FluentBundle.from_string("en", "hello = Hello, { $name }!", use_isolating=False),
        "ru": FluentBundle.from_string("ru", "hello = Привет, { $name }!", use_isolating=False),
    }
    I18nMiddleware(core, DbManager()).setup(dp)


async def pick_ru(_: CallbackQuery, __: Button, manager: DialogManager) -> None:
    await manager.middleware_data["i18n"].set_locale("ru")


LIBRARY = Library(T, setup, pick_ru, reads_per_update=1)
