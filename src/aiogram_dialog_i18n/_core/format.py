from abc import ABC, abstractmethod
from typing import Any

from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

from aiogram_dialog_i18n._core.resolve import DYNAMIC, Dynamic, Value, resolve


def require(middleware_data: dict, key: str, what: str) -> Any:
    value = middleware_data.get(key)
    if value is None:
        raise ValueError(f"{what} not found in manager.middleware_data[{key!r}], is the middleware set up?")
    return value


class BaseI18nFormat(Text, ABC):
    """
    Renders the translation ``key``, a subclass calls its i18n library.

    Params and ``locale`` are text widgets, magic filters or constants.
    ``key`` and ``locale`` are positional-only, so ``locale=...`` is a param.
    """

    def __init__(
        self,
        key: str,
        locale: Dynamic | str | None = None,
        /,
        *,
        when: WhenCondition = None,
        **params: Value,
    ) -> None:
        super().__init__(when=when)
        self.key = key

        # sorted once here, not on every render: the TextWidget protocol check is slow
        self.dynamic_locale = locale if isinstance(locale, DYNAMIC) else None
        self.locale = None if isinstance(locale, DYNAMIC) else locale
        self.dynamic = {name: value for name, value in params.items() if isinstance(value, DYNAMIC)}
        # None renders as "" on every core: Fluent raises on None (fluent-rs renders ""), gettext/jinja2 would print "None"
        self.static = {
            name: "" if value is None else value for name, value in params.items() if not isinstance(value, DYNAMIC)
        }

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        params = dict(self.static)
        for name, value in self.dynamic.items():
            result = await resolve(value, data, manager)
            params[name] = "" if result is None else result

        if manager.is_preview():
            args = ", ".join(f"{name}={'{' + name + '}' if value == '' else value}" for name, value in params.items())
            return f"{self.key}({args})" if args else self.key

        locale = self.locale if self.dynamic_locale is None else await resolve(self.dynamic_locale, data, manager)
        return self._translate(manager.middleware_data, locale, params)

    @abstractmethod
    def _translate(self, middleware_data: dict, locale: str | None, params: dict[str, Any]) -> str:
        """Translates ``self.key``, ``locale`` is None for the locale of the user."""
