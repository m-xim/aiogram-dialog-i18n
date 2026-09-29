from abc import ABC, abstractmethod
from typing import Any

from aiogram.types import Update


class BaseLocaleManager(ABC):
    """
    Gives the locale of the user to ``FluentogramMiddleware``, like the managers of aiogram-i18n.

    ``get_locale`` is called before the handler and again once per update on the first render of a widget,
    both times with the ``Update`` and the data of the handler.
    """

    @abstractmethod
    async def get_locale(self, event: Update, data: dict[str, Any]) -> str | None:
        """Returns the locale of the user, None for the root locale of the hub."""


class LanguageCodeManager(BaseLocaleManager):
    """Takes ``language_code`` of the user."""

    async def get_locale(self, event: Update, data: dict[str, Any]) -> str | None:  # noqa: ARG002
        user = data.get("event_from_user")
        return user.language_code if user else None
