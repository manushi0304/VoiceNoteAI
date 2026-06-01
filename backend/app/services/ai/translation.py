from argostranslate import translate


class TranslationService:
    @staticmethod
    def translate(text: str, source_lang: str, target_lang: str) -> str:
        return translate.translate(text, source_lang, target_lang)
