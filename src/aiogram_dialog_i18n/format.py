from typing import TypeAlias, TypeGuard

from aiogram_dialog.api.internal import TextWidget
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from magic_filter import MagicFilter

I18N_KEY = "i18n"

Value: TypeAlias = TextWidget | MagicFilter | str | float | bool


def is_dynamic(value: object) -> TypeGuard[MagicFilter | TextWidget]:
    return isinstance(value, (MagicFilter, TextWidget))


async def resolve(value: MagicFilter | TextWidget, data: dict, manager: DialogManager) -> object:
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
        locale: Value | None = None,
        /,
        *,
        when: WhenCondition = None,
        **params: Value,
    ) -> None:
        super().__init__(when=when)
        self.key = key

        # sorted once here, not on every render: the TextWidget protocol check is slow
        self.dynamic_locale = locale if is_dynamic(locale) else None
        self.locale = None if self.dynamic_locale else locale
        self.dynamic = {name: value for name, value in params.items() if is_dynamic(value)}

        # Fluent does not support None
        self.static: dict[str, object] = {
            name: "" if value is None else value for name, value in params.items() if name not in self.dynamic
        }

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        i18n = manager.middleware_data.get(I18N_KEY)
        if i18n is None:
            raise ValueError(
                f"I18nContext not found in manager.middleware_data[{I18N_KEY!r}], is I18nMiddleware set up?"
            )

        locale = self.locale if self.dynamic_locale is None else await resolve(self.dynamic_locale, data, manager)
        params = dict(self.static)
        for name, value in self.dynamic.items():
            result = await resolve(value, data, manager)
            params[name] = "" if result is None else result
        return i18n.get(self.key, locale, **params)
