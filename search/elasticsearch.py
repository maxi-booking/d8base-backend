"""The elasticsearch module."""
from elasticsearch_dsl import analysis

russian_token_filter = analysis.token_filter(
    "russian_lowercase",
    type="hunspell",
    language="ru_RU",
)
english_token_filter = analysis.token_filter(
    "english_lowercase",
    type="hunspell",
    language="en_US",
)
languages_analyzer = analysis.analyzer(
    "languages",
    type="custom",
    tokenizer="standard",
    filter=[russian_token_filter, english_token_filter],
)
