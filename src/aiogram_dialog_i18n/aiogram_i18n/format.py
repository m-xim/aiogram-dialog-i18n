from typing import Any

from aiogram_i18n import I18nMiddleware

from aiogram_dialog_i18n._core import BaseI18nFormat, require


class I18nFormat(BaseI18nFormat):
    """
    Renders the translation ``key`` via ``I18nContext`` of aiogram-i18n.

    The context is taken by the ``context_key`` of ``I18nMiddleware``, like aiogram-i18n finds its middleware.
    The locale is taken from the context on every render, so ``await i18n.set_locale(...)``
    in a handler is picked up by the window rendered after it.
    """

    async def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        middleware = I18nMiddleware.get_current()
        if middleware is None:
            raise ValueError("I18nMiddleware not found, is it created?")
        i18n = require(middleware_data, middleware.context_key, "I18nContext")
        return i18n.get(self.key, locale, **params)
