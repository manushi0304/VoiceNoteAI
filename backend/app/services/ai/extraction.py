import spacy

_nlp = spacy.load("en_core_web_sm")


class ExtractionService:
    @staticmethod
    def extract(text: str) -> dict:
        doc = _nlp(text)

        people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        dates = [ent.text for ent in doc.ents if ent.label_ in {"DATE", "TIME"}]

        return {
            "people": people,
            "dates": dates,
            "priority": "MEDIUM",
        }
