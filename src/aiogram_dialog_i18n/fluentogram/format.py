from typing import Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require
from aiogram_dialog_i18n.fluentogram.middleware import MIDDLEWARE_KEY, FluentogramMiddleware


class FluentogramFormat(BaseI18nFormat):
    """
    Renders the translation ``key`` via fluentogram.

    Takes the ``TranslatorRunner`` of the user, an explicit ``locale`` takes the ``TranslatorHub``,
    both from ``FluentogramMiddleware``. An unknown locale falls back to the root locale of the hub.
    """

    async def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        middleware: FluentogramMiddleware = require(middleware_data, MIDDLEWARE_KEY, "FluentogramMiddleware")
        if locale is not None:
            runner = middleware.hub.get_translator_by_locale(locale)
        else:
            runner = await middleware.render_runner(middleware_data)
        return runner.get(self.key, **params)
