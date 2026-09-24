from typing import cast

import pytest
from aiogram_dialog import DialogManager
from magic_filter import F

from aiogram_dialog_i18n.fluentogram import T
from aiogram_dialog_i18n.fluentogram.constants import HUB_KEY, RUNNER_KEY
from tests.fakes import FakeManager
from tests.fluentogram.hub import HUB


def make_manager(*, runner: bool = True, hub: bool = True) -> DialogManager:
    data = {}
    if runner:
        data[RUNNER_KEY] = HUB.get_translator_by_locale("ru")
    if hub:
        data[HUB_KEY] = HUB
    return cast("DialogManager", FakeManager(data))


async def test_none_is_empty():
    # a real Fluent bundle raises on None, the widget passes "" instead
    assert await T("hello", name=F["missing"]).render_text({}, make_manager()) == "Привет, !"


async def test_without_runner_raises():
    with pytest.raises(ValueError, match="TranslatorRunner not found"):
        await T("hello").render_text({}, make_manager(runner=False))


async def test_locale_without_hub_raises():
    with pytest.raises(ValueError, match="TranslatorHub not found"):
        await T("hello", "en").render_text({}, make_manager(hub=False))


async def test_preview_shows_key_and_params_without_middleware():
    manager = cast("DialogManager", FakeManager({}, preview=True))
    assert await T("hello", "en", name=F["n"]).render_text({}, manager) == "hello(name={name})"
