from collections.abc import Awaitable, Callable
from typing import Any, cast

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update
from fluentogram import TranslatorHub, TranslatorRunner

from aiogram_dialog_i18n.fluentogram.manager import BaseLocaleManager, LanguageCodeManager

MIDDLEWARE_KEY = "aiogram_dialog_i18n_fluentogram"
RENDER_RUNNER_KEY = "aiogram_dialog_i18n_fluentogram_runner"


class FluentogramMiddleware(BaseMiddleware):
    """
    Puts the ``TranslatorRunner`` of the user under ``runner_key`` and the ``TranslatorHub`` under ``hub_key``.

    The locale is given by ``manager``, ``language_code`` of the user by default.
    Widgets ask it again once per update on the first render, so a locale changed in a handler is shown at once.
    """

    def __init__(
        self,
        hub: TranslatorHub,
        manager: BaseLocaleManager | None = None,
        *,
        runner_key: str = "i18n",
        hub_key: str = "translator_hub",
    ) -> None:
        self.hub = hub
        self.manager = manager or LanguageCodeManager()
        self.runner_key = runner_key
        self.hub_key = hub_key

    async def load_runner(self, event: Update, data: dict[str, Any]) -> TranslatorRunner:
        """Reads the locale and puts its ``TranslatorRunner`` into the data."""
        locale = await self.manager.get_locale(event, data)
        runner = data[self.runner_key] = self.hub.get_translator_by_locale(locale=locale or self.hub.root_locale)
        return runner

    async def render_runner(self, data: dict[str, Any]) -> TranslatorRunner:
        """The ``TranslatorRunner`` for widgets: the locale is read again on the first render of the update."""
        runner = data.get(RENDER_RUNNER_KEY)
        if runner is None:
            runner = data[RENDER_RUNNER_KEY] = await self.load_runner(data["event_update"], data)
        return runner

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data[self.hub_key] = self.hub
        data[MIDDLEWARE_KEY] = self
        await self.load_runner(cast("Update", event), data)
        return await handler(event, data)

    def setup(self, dispatcher: Dispatcher) -> None:
        """Registers the middleware for every update, so dialogs are translated on messages, callbacks and bg updates."""
        dispatcher.update.outer_middleware(self)
