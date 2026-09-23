# aiogram-dialog-i18n

Translated text widget for [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) powered by [aiogram-i18n](https://github.com/aiogram/i18n).

```bash
uv add aiogram-dialog-i18n
# or
pip install aiogram-dialog-i18n
```

## Usage

Set up `I18nMiddleware` from [aiogram-i18n](https://github.com/aiogram/i18n) as usual: the widget takes `I18nContext` from `middleware_data["i18n"]` (its default `context_key`).

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

## `I18nFormat(key, locale=None, /, *, when=None, **params)`

Renders the translation `key` with `params` in the current locale of the user. It is a regular aiogram-dialog text widget, so it works wherever a text is expected: `Window`, `Button`, `List`, `Multi`, …. `T` is a short alias.

### Params

Every param is a `Value`:

- a text widget is rendered (`Format`, `Const`, another `I18nFormat`, …);
- a `MagicFilter` is resolved against window data;
- anything else (`str`, `int`, `float`, `bool`) is passed as is.

`None` becomes an empty string.

```python
I18nFormat(
    "hello-user",
    name=F["user"].full_name,  # magic filter over window data
    balance=Format("{balance:.2f}"),  # any text widget
    vip=True,  # constant
)
```

### Locale

By default the locale of the user is used. The second positional argument overrides it and is a `Value` too:

```python
I18nFormat("k", "en")  # fixed locale
I18nFormat("k", F["lang"])  # locale from window data
I18nFormat("k", locale=F["lang"])  # not a locale: a message param named "locale"
```

`key` and `locale` are positional-only, like in `I18nContext.get`, so a message can still have a param called `locale`. `when` is the usual aiogram-dialog visibility condition, not a message param.
