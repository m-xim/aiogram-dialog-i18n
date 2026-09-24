from typing import cast

import pytest
from aiogram_dialog import DialogManager
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from magic_filter import F

from aiogram_dialog_i18n.fluentogram import HUB_KEY, RUNNER_KEY, T
from tests.conftest import FakeManager

HUB = TranslatorHub(
    {"en": "en", "ru": ("ru", "en")},
    [
        FluentTranslator("en", FluentBundle.from_string("en", "hello = Hello, { $name }!", use_isolating=False)),
        FluentTranslator("ru", FluentBundle.from_string("ru", "hello = Привет, { $name }!", use_isolating=False)),
    ],
    root_locale="en",
)


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
