"""The routers tests module."""
from d8b.trans import translate


def test_translate():
    """Should translate a text."""
    assert translate("Moscow", src="en", dest="de") == "Moskau"
    assert translate("Moscow", src="en", dest="ru") == "Москва"
    assert translate("aaabbb", src="en", dest="de") == "aaabbb"
