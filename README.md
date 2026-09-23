# aiogram-dialog-i18n

[![PyPI version](https://img.shields.io/pypi/v/aiogram-dialog-i18n?color=blue)](https://pypi.org/project/aiogram-dialog-i18n)
[![codecov](https://codecov.io/github/m-xim/aiogram-dialog-i18n/graph/badge.svg)](https://codecov.io/github/m-xim/aiogram-dialog-i18n)
[![Tests Status](https://github.com/m-xim/aiogram-dialog-i18n/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-dialog-i18n/actions)
[![License](https://img.shields.io/github/license/m-xim/aiogram-dialog-i18n.svg)](/LICENSE)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

Translated text widget for [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) powered by [aiogram-i18n](https://github.com/aiogram/i18n).

## Installation

```bash
uv add aiogram-dialog-i18n
# or
pip install aiogram-dialog-i18n
```

Requires Python 3.10+, `aiogram-dialog` 2.0+ and `aiogram-i18n` 1.4+.

## Usage

`I18nFormat` (short alias: `T`) renders a translation key wherever aiogram-dialog expects a text: `Window`, `Button`, `List`, `Multi`, and so on. Params can be plain values, magic filters over window data or other text widgets.

Set up `I18nMiddleware` from [aiogram-i18n](https://github.com/aiogram/i18n) as usual. The widget takes `I18nContext` from `middleware_data["i18n"]`, which is the default `context_key`, and raises `ValueError` if it is missing.

```ftl
hello-user = Hello, { $name }! Balance: { $balance }
payment-method = • { $method }
pay-btn = Pay
```

```python
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, List
from magic_filter import F

from aiogram_dialog_i18n import I18nFormat, T

Window(
    I18nFormat("hello-user", name=F["user"].full_name, balance=Format("{balance:.2f}")),
    List(T("payment-method", method=F["item"]), F["methods"]),
    Button(T("pay-btn"), id="pay", when=F["methods"]),
    state=...,
)
```

## Signature

```python
I18nFormat(key, locale=None, /, *, when=None, **params)
```

- `key` is the translation key;
- `locale` overrides the locale of the user, see [Locale](#locale);
- `when` is the usual aiogram-dialog visibility condition, not a message param;
- `params` are the message params, see [Params](#params).

`key` and `locale` are positional-only, like in `I18nContext.get`, so a message can still have a param called `locale`.

## Params

Every param is one of:

- a text widget, it is rendered (`Format`, `Const`, another `I18nFormat`, …);
- a `MagicFilter`, it is resolved against window data;
- a constant (`str`, `int`, `float`, `bool`), it is passed as is.

`None` becomes an empty string.

```python
I18nFormat(
    "hello-user",
    name=F["user"].full_name,  # magic filter over window data
    balance=Format("{balance:.2f}"),  # any text widget
    vip=True,  # constant
)
```

## Locale

By default the locale of the user is used. The second positional argument overrides it, it can be a constant, a magic filter or a text widget:

```python
I18nFormat("k", "en")  # fixed locale
I18nFormat("k", F["lang"])  # locale from window data
I18nFormat("k", locale=F["lang"])  # not a locale: a message param named "locale"
```

## Preview

There is no `I18nContext` in `aiogram_dialog.tools.render_preview`, so the widget shows the key with its params instead of a translation. An empty value is shown as `{name}`, like `Format` does. The window from [Usage](#usage) looks like this:

<img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-keys.png" width="360" alt="Preview of the window: the key with its params">

```
hello-user(name={name}, balance={balance:.2f})
```

The list and the button are not shown, because there is no window data in a preview and `F["methods"]` is empty.

With a real `I18nContext` the same window is rendered with translations, here in English and Russian:

| English | Русский |
|---|---|
| <img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-en.png" width="360" alt="Window in English"> | <img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-ru.png" width="360" alt="Window in Russian"> |
