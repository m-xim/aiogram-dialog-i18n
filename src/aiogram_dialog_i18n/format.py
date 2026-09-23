from typing import Any, TypeAlias

from aiogram_dialog.api.internal import TextWidget
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from magic_filter import MagicFilter

I18N_KEY = "i18n"

Dynamic: TypeAlias = TextWidget | MagicFilter
Constant: TypeAlias = str | float | bool
Value: TypeAlias = Dynamic | Constant | None

DYNAMIC = (MagicFilter, TextWidget)  # for isinstance, which narrows the type in both branches


async def resolve(value: Dynamic, data: dict, manager: DialogManager) -> Any:
    # MagicFilter goes first: on Python < 3.12 it also passes isinstance(..., TextWidget) via __getattr__
    if isinstance(value, MagicFilter):
        return value.resolve(data)
    return await value.render_text(data, manager)


class I18nFormat(Text):
    """
    Renders the translation ``key`` via ``I18nContext``.

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
        # Fluent does not support None
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

        i18n = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            raise ValueError(
                f"I18nContext not found in manager.middleware_data[{I18N_KEY!r}], is I18nMiddleware set up?"
            )

        locale = self.locale if self.dynamic_locale is None else await resolve(self.dynamic_locale, data, manager)
        return i18n.get(self.key, locale, **params)
