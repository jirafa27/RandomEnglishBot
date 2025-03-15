import re

from langid.langid import LanguageIdentifier, model
from deep_translator import GoogleTranslator

from exceptions.exceptions import NotEnglishTextException, NotRussianTextException


class Translator:
    def is_english_text(self, text: str) -> bool:
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        # identifier.set_languages(['en', 'ru'])
        pattern = r"^(?=.*[A-Za-z])[A-Za-z0-9\s\.,;:'\"?!()\-]+$"
        if not re.match(pattern, text):
            return False

        ans = identifier.classify(text)
        return ans[0] == "en" and not (ans[0] != "en" and ans[1] < 0.8)

    def is_russian_text(self, text: str) -> bool:
        identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        pattern = r"^(?=.*[А-Яа-я])[А-Яа-я0-9\s\.,;:'\"?!()\-]+$"
        if not re.match(pattern, text):
            return False
        return True

    def translate_en_ru(self, text: str) -> str:
        if not self.is_english_text(text):
            raise NotEnglishTextException
        translated = GoogleTranslator(source="en", target="ru").translate(text)
        return translated

    def translate_ru_en(self, text: str) -> str:
        if not self.is_russian_text(text):
            raise NotRussianTextException
        translated = GoogleTranslator(source="ru", target="en").translate(text)
        return translated
