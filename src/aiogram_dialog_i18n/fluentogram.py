from typing import Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require

RUNNER_KEY = "i18n"
HUB_KEY = "_translator_hub"


class FluentogramFormat(BaseI18nFormat):
    """
    Renders the translation ``key`` via fluentogram.

    The ``TranslatorRunner`` of the user is taken by ``RUNNER_KEY``.
    An explicit ``locale`` needs the ``TranslatorHub`` by ``HUB_KEY``, an unknown locale falls back to its root locale.
    """

    def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        if locale is None:
            runner = require(middleware_data, RUNNER_KEY, "TranslatorRunner")
        else:
            runner = require(middleware_data, HUB_KEY, "TranslatorHub").get_translator_by_locale(locale)
        return runner.get(self.key, **params)


T = FluentogramFormat

__all__ = ["HUB_KEY", "RUNNER_KEY", "FluentogramFormat", "T"]
