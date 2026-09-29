import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import BgManagerFactory, Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator
from aiogram_dialog.test_tools.memory_storage import JsonMemoryStorage
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import List
from magic_filter import F

from aiogram_dialog_i18n._core import BaseI18nFormat

EN = "Hello, Bob!\nHello, A!\nHello, B!\n[Hello, RU!]"
RU = "Привет, Bob!\nПривет, A!\nПривет, B!\n[Привет, RU!]"


@dataclass(frozen=True)
class Library:
    widget: type[BaseI18nFormat]
    setup: Callable[[Dispatcher], None]
    """Sets up the middleware, its locale manager takes the locale from ``db[user_id]``."""
    pick_ru: OnClick
    """The click on "RU", changes the locale the way the library does it."""
    reads_per_update: int
    """How many times the locale is read from ``db`` for one update with a window."""


class Db(dict[int, str]):
    """The locales of the users, like a database, counts the reads."""

    reads = 0

    def __getitem__(self, user_id: int) -> str:
        self.reads += 1
        return super().__getitem__(user_id)


class SG(StatesGroup):
    main = State()


async def start(_: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(SG.main, mode=StartMode.RESET_STACK)


async def get_names(**_: Any) -> dict[str, Any]:
    return {"names": ["A", "B"]}


class App:
    def __init__(self, library: Library) -> None:
        widget = library.widget
        self.reads_per_update = library.reads_per_update
        self.db = Db({1: "en"})
        self.messages = MockMessageManager()
        self.dp = Dispatcher(storage=JsonMemoryStorage(), db=self.db)
        self.dialog = Dialog(
            Window(
                widget("hello", name="Bob"),
                List(widget("hello", name=F["item"]), F["names"]),
                Button(text=widget("hello", name="RU"), id="ru", on_click=library.pick_ru),
                getter=get_names,
                state=SG.main,
            ),
        )
        self.dp.include_router(self.dialog)
        self.dp.message.register(start, CommandStart())
        self.bg: BgManagerFactory = setup_dialogs(self.dp, message_manager=self.messages)
        library.setup(self.dp)
        self.client = BotClient(self.dp)
        self.last: Message | None = None

    def shown(self) -> str:
        """The only message shown since the last call: its text and buttons."""
        self.last = self.messages.one_message()
        self.messages.reset_history()
        assert self.last.reply_markup
        buttons = [button.text for row in self.last.reply_markup.inline_keyboard for button in row]
        return f"{self.last.text}\n[{', '.join(buttons)}]"

    async def click(self, text: str) -> None:
        """Clicks the button of the last shown message, ``text`` is a regex of the whole button text."""
        assert self.last
        callback_id = await self.client.click(self.last, InlineButtonTextLocator(text))
        self.messages.assert_answered(callback_id)

    async def bg_update(self) -> None:
        await self.bg.bg(self.client.bot, 1, 1).update({})
        # BgManager.update() only schedules the update: call_soon, then create_task
        await asyncio.sleep(0)
        await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})

    async def fg_show(self) -> None:
        async with self.bg.bg(self.client.bot, 1, 1).fg() as manager:
            await manager.show()
