from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

HUB = TranslatorHub(
    {"en": "en", "ru": ("ru", "en")},
    [
        FluentTranslator("en", FluentBundle.from_string("en", "hello = Hello, { $name }!", use_isolating=False)),
        FluentTranslator("ru", FluentBundle.from_string("ru", "hello = Привет, { $name }!", use_isolating=False)),
    ],
    root_locale="en",
)
