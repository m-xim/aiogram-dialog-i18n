from typing import cast

import pytest
from aiogram_dialog import DialogManager

from aiogram_dialog_i18n.aiogram_i18n.constants import CONTEXT_KEY
from tests.fakes import FakeI18n, FakeManager


@pytest.fixture
def manager() -> DialogManager:
    return cast("DialogManager", FakeManager({CONTEXT_KEY: FakeI18n()}))


@pytest.fixture
def manager_without_i18n() -> DialogManager:
    return cast("DialogManager", FakeManager({}))


@pytest.fixture
def preview_manager() -> DialogManager:
    return cast("DialogManager", FakeManager({}, preview=True))
