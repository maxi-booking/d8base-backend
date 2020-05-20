"""The services tests module."""
from communication.notifications.services import (render_template,
                                                  translate_subject)


def test_translate_subject():
    """Should translate a subject."""
    assert translate_subject('ru', 'name') == 'имя'
    assert translate_subject('de', 'country') == 'staat'


def test_render_template():
    """Should translate a template."""
    expected = 'A new message notification.'
    assert expected in render_template(
        'de',
        'message_notification',
        'push',
        {},
    )
