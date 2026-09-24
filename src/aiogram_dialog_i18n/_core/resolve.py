from typing import Any, TypeAlias

from aiogram_dialog.api.internal import TextWidget
from aiogram_dialog.api.protocols import DialogManager
from magic_filter import MagicFilter

Dynamic: TypeAlias = TextWidget | MagicFilter
Constant: TypeAlias = str | float | bool
Value: TypeAlias = Dynamic | Constant | None

DYNAMIC = (MagicFilter, TextWidget)  # for isinstance, which narrows the type in both branches


async def resolve(value: Dynamic, data: dict, manager: DialogManager) -> Any:
    # MagicFilter goes first: on Python < 3.12 it also passes isinstance(..., TextWidget) via __getattr__
    if isinstance(value, MagicFilter):
        return value.resolve(data)
    return await value.render_text(data, manager)
