from typing import TYPE_CHECKING, Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require

if TYPE_CHECKING:
    from aiogram_i18n import I18nMiddleware

# the default ``middleware_key`` of ``I18nMiddleware``, its ``setup`` puts the middleware into the dispatcher data
MIDDLEWARE_KEY = "i18n_middleware"


class I18nFormat(BaseI18nFormat):
    """
    Renders the translation ``key`` via ``I18nContext`` of aiogram-i18n.

    The context is taken by the ``context_key`` of the ``I18nMiddleware`` of the dispatcher of the update,
    so several bots with their own dispatchers and keys work in one process.
    The locale is taken from the context on every render, so ``await i18n.set_locale(...)``
    in a handler is picked up by the window rendered after it.
    """

    async def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        middleware: I18nMiddleware = require(middleware_data, MIDDLEWARE_KEY, "I18nMiddleware")
        i18n = require(middleware_data, middleware.context_key, "I18nContext")
        return i18n.get(self.key, locale, **params)
