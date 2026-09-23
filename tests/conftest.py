from typing import cast

import pytest
from aiogram_dialog import DialogManager

from aiogram_dialog_i18n.format import I18N_KEY


class FakeI18n:
    def get(self, key: str, locale: str | None = None, /, **kwargs: object) -> str:
        params = ",".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return f"{key}[{locale}]({params})"


class FakeManager:
    def __init__(self, middleware_data: dict) -> None:
        self.middleware_data = middleware_data

    def is_preview(self) -> bool:
        return False


@pytest.fixture
def manager() -> DialogManager:
    return cast("DialogManager", FakeManager({I18N_KEY: FakeI18n()}))


@pytest.fixture
def manager_without_i18n() -> DialogManager:
    return cast("DialogManager", FakeManager({}))
