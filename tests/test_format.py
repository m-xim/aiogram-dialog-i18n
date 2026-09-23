import pytest
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format, List
from magic_filter import F

from aiogram_dialog_i18n import I18nFormat, T


async def test_resolves_all_value_kinds(manager: DialogManager):
    widget = I18nFormat("hello", widget=Format("{n}!"), magic=F["n"] + 1, const="c", none=F["missing"])
    assert await widget.render_text({"n": 1}, manager) == "hello[None](const=c,magic=2,none=,widget=1!)"


async def test_locale(manager: DialogManager):
    assert await I18nFormat("k", F["lang"]).render_text({"lang": "en"}, manager) == "k[en]()"


async def test_locale_keyword_is_fluent_argument(manager: DialogManager):
    assert await I18nFormat("k", locale="en").render_text({}, manager) == "k[None](locale=en)"


async def test_inside_list(manager: DialogManager):
    widget = List(T("pay", method=F["item"], user=F["data"]["user"]), F["methods"], sep=", ")
    text = await widget.render_text({"methods": ["card", "sbp"], "user": "u"}, manager)
    assert text == "pay[None](method=card,user=u), pay[None](method=sbp,user=u)"


async def test_when(manager: DialogManager):
    assert await I18nFormat("k", when=F["show"]).render_text({"show": False}, manager) == ""


async def test_without_middleware_raises(manager_without_i18n: DialogManager):
    with pytest.raises(ValueError, match="I18nContext not found"):
        await I18nFormat("k").render_text({}, manager_without_i18n)


async def test_preview_shows_key_and_params_without_middleware(preview_manager: DialogManager):
    widget = I18nFormat("hello", "en", name=F["n"], widget=Format("{n}!"), const="c")
    assert await widget.render_text({"n": 5}, preview_manager) == "hello(const=c, name=5, widget=5!)"
    assert await widget.render_text({}, preview_manager) == "hello(const=c, name={name}, widget={n}!)"
    assert await I18nFormat("hello").render_text({}, preview_manager) == "hello"
