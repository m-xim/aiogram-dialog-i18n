from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject

from aiogram_dialog_i18n.fluentogram import constants

if TYPE_CHECKING:
    from fluentogram import TranslatorHub


class FluentogramMiddleware(BaseMiddleware):
    """
    Puts the ``TranslatorRunner`` of the user and the ``TranslatorHub`` into the data.

    The locale is ``language_code`` of the user, override ``get_locale`` to take it from a database.
    """

    def __init__(self, hub: "TranslatorHub") -> None:
        self.hub = hub

    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str | None:  # noqa: ARG002
        """Returns the locale of the user, None for the root locale of the hub."""
        user = data.get("event_from_user")
        return user.language_code if user else None

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        locale = await self.get_locale(event, data)
        data[constants.HUB_KEY] = self.hub
        data[constants.RUNNER_KEY] = self.hub.get_translator_by_locale(locale or self.hub.root_locale)
        return await handler(event, data)

    def setup(self, dispatcher: Dispatcher) -> None:
        """Registers the middleware for every update, so dialogs are translated on messages, callbacks and bg updates."""
        dispatcher.update.outer_middleware(self)
