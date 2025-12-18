import re

def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text

def equals_loose(a: str, b: str) -> bool:
    return normalize_text(a) == normalize_text(b)

def contains_keywords(answer: str, keywords: list[str]) -> bool:
    ans_norm = normalize_text(answer)
    return all(k.lower() in ans_norm for k in keywords)


