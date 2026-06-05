class TranslationService:
    @staticmethod
    def translate(text: str, source_lang: str, target_lang: str) -> str:
        try:
            from argostranslate import translate
            return translate.translate(text, source_lang, target_lang)
        except Exception as e:
            print(f"⚠️ Argos Translate failed: {e}. Returning original text!")
            return text
