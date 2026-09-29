from typing import TYPE_CHECKING, cast

import pytest
from aiogram_dialog import DialogManager
from aiogram_i18n import I18nMiddleware

from aiogram_dialog_i18n.aiogram_i18n.format import MIDDLEWARE_KEY
from tests.fakes import FakeCore, FakeManager

if TYPE_CHECKING:
    from aiogram_i18n.cores import BaseCore


def make_manager(context_key: str = "i18n") -> DialogManager:
    """The data of an update of a user with the locale "ru" after ``I18nMiddleware(context_key=...).setup(dp)``."""
    middleware = I18nMiddleware(cast("BaseCore", FakeCore()), context_key=context_key)
    context = middleware.new_context(locale="ru", data={})
    return cast("DialogManager", FakeManager({MIDDLEWARE_KEY: middleware, context_key: context}))


@pytest.fixture
def manager() -> DialogManager:
    return make_manager()


@pytest.fixture
def preview_manager() -> DialogManager:
    return cast("DialogManager", FakeManager({}, preview=True))
