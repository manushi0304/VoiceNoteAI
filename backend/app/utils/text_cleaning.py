import re

def clean_voice_text(text: str, label: str) -> str:
    # 1. Strip whitespace
    text = text.strip()
    if not text:
        return "Untitled"
        
    # Pre-clean generic prefixes and conversational markers using regex
    text = re.sub(r"^(i\s+decided\s+to\s+do\s+to\b|i\s+decided\s+to\s+do\b)", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^(to\s*do\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^(reminder\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^(note\s*[-:]?\s*)", "", text, flags=re.IGNORECASE).strip()

    lower_text = text.lower()
    
    if label == "todo":
        todo_prefixes = [
            r"write down to do to\b",
            r"write down to do\b",
            r"write it to do to\b",
            r"write it to do\b",
            r"make a high priority to do to\b",
            r"make a high priority to do\b",
            r"make a medium priority to do to\b",
            r"make a medium priority to do\b",
            r"make a low priority to do to\b",
            r"make a low priority to do\b",
            r"make a hype priority to do to\b",
            r"make a hype priority to do\b",
            r"make a priority to do to\b",
            r"make a priority to do\b",
            r"create a todo to\b",
            r"create a todo\b",
            r"add a todo to\b",
            r"add a todo\b",
            r"to do to\b",
            r"to do\b",
            r"todo to\b",
            r"todo\b",
        ]
        for pattern in todo_prefixes:
            match = re.match(pattern, lower_text)
            if match:
                text = text[match.end():].strip()
                lower_text = text.lower()
                break
                
        # Also clean leading "to " (e.g. "to finish homework" -> "finish homework")
        if lower_text.startswith("to "):
            text = text[3:].strip()
            lower_text = text.lower()
            
    elif label == "reminder":
        reminder_prefixes = [
            r"set a reminder to\b",
            r"set a reminder\b",
            r"the remind me to\b",
            r"the remind me\b",
            r"the mind me to\b",
            r"the mind me\b",
            r"remind me to\b",
            r"remind me\b",
            r"mind me to\b",
            r"mind me\b",
            r"reminder to\b",
            r"reminder\b",
        ]
        for pattern in reminder_prefixes:
            match = re.match(pattern, lower_text)
            if match:
                text = text[match.end():].strip()
                lower_text = text.lower()
                break
                
        # Also clean leading "to "
        if lower_text.startswith("to "):
            text = text[3:].strip()
            lower_text = text.lower()

    elif label == "note":
        note_prefixes = [
            r"write down that\b",
            r"write down\b",
            r"write a note that\b",
            r"write a note\b",
            r"create a note that\b",
            r"create a note\b",
            r"take a note\b",
            r"put a note\b",
            r"note that\b",
            r"note\b",
        ]
        for pattern in note_prefixes:
            match = re.match(pattern, lower_text)
            if match:
                text = text[match.end():].strip()
                lower_text = text.lower()
                break
                
    # 3. Clean leading/trailing spaces and ending punctuation (. ! ? ,) for titles
    text = text.strip()
    if label in ("todo", "reminder"):
        text = re.sub(r"[.!?,]+$", "", text).strip()
        
    if not text:
        return "Untitled"
        
    # Capitalize the first letter for neatness
    return text[0].upper() + text[1:]
