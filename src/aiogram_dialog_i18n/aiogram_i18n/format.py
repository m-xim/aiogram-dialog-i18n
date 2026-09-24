from typing import Any

from aiogram_dialog_i18n._core import BaseI18nFormat, require
from aiogram_dialog_i18n.aiogram_i18n import constants


class I18nFormat(BaseI18nFormat):
    """Renders the translation ``key`` via ``I18nContext`` of aiogram-i18n."""

    def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        i18n = require(middleware_data, constants.CONTEXT_KEY, "I18nContext")
        return i18n.get(self.key, locale, **params)
