from typing import Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require

CONTEXT_KEY = "i18n"


class I18nFormat(BaseI18nFormat):
    """Renders the translation ``key`` via ``I18nContext`` of aiogram-i18n."""

    def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        i18n = require(middleware_data, CONTEXT_KEY, "I18nContext")
        return i18n.get(self.key, locale, **params)


T = I18nFormat

__all__ = ["CONTEXT_KEY", "I18nFormat", "T"]
