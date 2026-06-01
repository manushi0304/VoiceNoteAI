class VoiceCommandService:
    @staticmethod
    def parse(text: str) -> dict:
        text = text.lower()

        if text.startswith("add"):
            return {"intent": "create", "params": {"text": text}}
        if text.startswith("delete"):
            return {"intent": "delete", "params": {"text": text}}

        return {"intent": "unknown", "params": {}}
