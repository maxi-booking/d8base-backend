"""The d8b trans module."""
from collections import defaultdict
from typing import DefaultDict, Tuple

from translate import Translator


def translate(text: str, src: str, dest: str) -> str:
    """Translate the text."""
    clean: DefaultDict[str, Tuple[str, ...]] = defaultdict(tuple)
    clean["ru"] = ("г.", )
    translator = Translator(from_lang=src, to_lang=dest)
    result = translator.translate(text)
    for i in clean[dest]:
        result = result.replace(i, "")
    return result.strip()
