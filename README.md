# aiogram-dialog-i18n

[![PyPI version](https://img.shields.io/pypi/v/aiogram-dialog-i18n?color=blue)](https://pypi.org/project/aiogram-dialog-i18n)
[![codecov](https://codecov.io/github/m-xim/aiogram-dialog-i18n/graph/badge.svg)](https://codecov.io/github/m-xim/aiogram-dialog-i18n)
[![Tests Status](https://github.com/m-xim/aiogram-dialog-i18n/actions/workflows/tests.yml/badge.svg)](https://github.com/m-xim/aiogram-dialog-i18n/actions)
[![License](https://img.shields.io/github/license/m-xim/aiogram-dialog-i18n.svg)](/LICENSE)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

Translated text widget for [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) powered by [aiogram-i18n](https://github.com/aiogram/i18n) or [fluentogram](https://github.com/Arustinal/fluentogram).

The examples use these translations:

```ftl
hello-user = Hello, { $name }! Balance: { $balance }
payment-method = • { $method }
pay-btn = Pay
```

## aiogram-i18n

### Installation

```bash
uv add "aiogram-dialog-i18n[aiogram-i18n]"
# or
pip install "aiogram-dialog-i18n[aiogram-i18n]"
```

### Setup

Set up `I18nMiddleware` as usual.

### Usage

`I18nFormat`, short alias `T`:

```python
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, List
from magic_filter import F

from aiogram_dialog_i18n.aiogram_i18n import I18nFormat, T

Window(
    I18nFormat("hello-user", name=F["user"].full_name, balance=Format("{balance:.2f}")),
    List(T("payment-method", method=F["item"]), F["methods"]),
    Button(T("pay-btn"), id="pay", when=F["methods"]),
    state=...,
)
```

## fluentogram

### Installation

```bash
uv add "aiogram-dialog-i18n[fluentogram]"
# or
pip install "aiogram-dialog-i18n[fluentogram]"
```

### Setup

`FluentogramMiddleware` puts the `TranslatorRunner` of the user and the `TranslatorHub` into the data, set it up after the other middlewares:

```python
from aiogram_dialog_i18n.fluentogram import FluentogramMiddleware

FluentogramMiddleware(hub).setup(dp)
```

To take the locale from a database, override `get_locale`:

```python
class DbFluentogramMiddleware(FluentogramMiddleware):
    async def get_locale(self, event, data):
        user = await data["repo"].get_user(data["event_from_user"].id)
        return user.language if user else None


DbFluentogramMiddleware(hub).setup(dp)
```

### Usage

`FluentogramFormat`, short alias `T`:

```python
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, List
from magic_filter import F

from aiogram_dialog_i18n.fluentogram import FluentogramFormat, T

Window(
    FluentogramFormat("hello-user", name=F["user"].full_name, balance=Format("{balance:.2f}")),
    List(T("payment-method", method=F["item"]), F["methods"]),
    Button(T("pay-btn"), id="pay", when=F["methods"]),
    state=...,
)
```

## Arguments

Both widgets take the same arguments:

```python
I18nFormat(key, locale=None, /, *, when=None, **params)
FluentogramFormat(key, locale=None, /, *, when=None, **params)
```

- `key` is the translation key;
- `locale` overrides the locale of the user, see [Locale](#locale);
- `when` is the usual aiogram-dialog visibility condition, not a message param;
- `params` are the message params, see [Params](#params).

`key` and `locale` are positional-only, so a message can still have a param called `locale`.

### Params

Every param is one of:

- a text widget, it is rendered (`Format`, `Const`, another translated widget, …);
- a `MagicFilter`, it is resolved against window data;
- a constant (`str`, `int`, `float`, `bool`), it is passed as is.

`None` becomes an empty string on every core, so in Jinja2 check it with `{% if x %}`, not `is none`.

### Locale

By default the locale of the user is used. The second positional argument overrides it, it can be a constant, a magic filter or a text widget:

```python
T("k", "en")  # fixed locale
T("k", F["lang"])  # locale from window data
T("k", locale=F["lang"])  # not a locale: a message param named "locale"
```

## Preview

There is no middleware data in `aiogram_dialog.tools.render_preview`, so both widgets show the key with its params instead of a translation. An empty value is shown as `{name}`, like `Format` does. The window from the examples looks like this:

<img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-keys.png" width="360" alt="Preview of the window: the key with its params">

With the middleware the same window is rendered with translations, here in English and Russian:

| English | Русский |
|---|---|
| <img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-en.png" width="360" alt="Window in English"> | <img src="https://raw.githubusercontent.com/m-xim/aiogram-dialog-i18n/main/assets/preview-ru.png" width="360" alt="Window in Russian"> |
