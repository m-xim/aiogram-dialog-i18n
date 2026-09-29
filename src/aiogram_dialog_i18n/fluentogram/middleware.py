from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, cast

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update

from aiogram_dialog_i18n.fluentogram import constants
from aiogram_dialog_i18n.fluentogram.manager import BaseLocaleManager, LanguageCodeManager

if TYPE_CHECKING:
    from fluentogram import TranslatorHub, TranslatorRunner


class FluentogramMiddleware(BaseMiddleware):
    """
    Puts the ``TranslatorRunner`` of the user and the ``TranslatorHub`` into the data.

    The locale is given by ``manager``, ``language_code`` of the user by default.
    Widgets ask it again once per update on the first render, so a locale changed in a handler is shown at once.
    """

    def __init__(self, hub: "TranslatorHub", manager: BaseLocaleManager | None = None) -> None:
        self.hub = hub
        self.manager = manager or LanguageCodeManager()

    async def load_runner(self, event: Update, data: dict[str, Any]) -> "TranslatorRunner":
        """Reads the locale and puts its ``TranslatorRunner`` into the data."""
        locale = await self.manager.get_locale(event, data)
        runner = data[constants.RUNNER_KEY] = self.hub.get_translator_by_locale(locale=locale or self.hub.root_locale)
        return runner

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data[constants.HUB_KEY] = self.hub
        data[constants.MIDDLEWARE_KEY] = self
        await self.load_runner(cast("Update", event), data)
        return await handler(event, data)

    def setup(self, dispatcher: Dispatcher) -> None:
        """Registers the middleware for every update, so dialogs are translated on messages, callbacks and bg updates."""
        dispatcher.update.outer_middleware(self)
