from typing import Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require
from aiogram_dialog_i18n.fluentogram import constants


class FluentogramFormat(BaseI18nFormat):
    """
    Renders the translation ``key`` via fluentogram.

    Takes the ``TranslatorRunner`` of the user, an explicit ``locale`` takes the ``TranslatorHub``,
    both are put by ``FluentogramMiddleware``. An unknown locale falls back to the root locale of the hub.
    """

    async def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        if locale is not None:
            runner = require(middleware_data, constants.HUB_KEY, "TranslatorHub").get_translator_by_locale(locale)
        elif (middleware := middleware_data.pop(constants.MIDDLEWARE_KEY, None)) is not None:
            runner = await middleware.load_runner(middleware_data["event_update"], middleware_data)
        else:
            runner = require(middleware_data, constants.RUNNER_KEY, "TranslatorRunner")
        return runner.get(self.key, **params)
