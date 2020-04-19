"""The language settings module."""
from django.utils.translation import ugettext_lazy as _

USE_I18N = True

USE_L10N = True

LANGUAGE_CODE = 'en'

MODELTRANSLATION_DEFAULT_LANGUAGE = LANGUAGE_CODE

MODELTRANSLATION_LANGUAGES = ('en', 'de', 'fr', 'ru')

LANGUAGES = (
    ('af', _('Afrikaans')),
    ('sq', _('Albanian')),
    ('am', _('Amharic')),
    ('ar', _('Arabic')),
    ('hy', _('Armenian')),
    ('az', _('Azerbaijani')),
    ('eu', _('Basque')),
    ('be', _('Belarusian')),
    ('bn', _('Bengali')),
    ('bs', _('Bosnian')),
    ('bg', _('Bulgarian')),
    ('ca', _('Catalan')),
    ('zh', _('Chinese')),
    ('co', _('Corsican')),
    ('hr', _('Croatian')),
    ('cs', _('Czech')),
    ('da', _('Danish')),
    ('nl', _('Dutch')),
    ('en', _('English')),
    ('eo', _('Esperanto')),
    ('et', _('Estonian')),
    ('tl', _('Filipino')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('fy', _('Frisian')),
    ('gl', _('Galician')),
    ('ka', _('Georgian')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('gu', _('Gujarati')),
    ('ht', _('Haitian Creole')),
    ('ha', _('Hausa')),
    ('he', _('Hebrew')),
    ('hi', _('Hindi')),
    ('hu', _('Hungarian')),
    ('is', _('Icelandic')),
    ('id', _('Indonesian')),
    ('ga', _('Irish')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('jv', _('Javanese')),
    ('kn', _('Kannada')),
    ('kk', _('Kazakh')),
    ('km', _('Khmer')),
    ('ko', _('Korean')),
    ('ku', _('Kurdish (Kurmanji)')),
    ('ky', _('Kyrgyz')),
    ('lo', _('Lao')),
    ('la', _('Latin')),
    ('lv', _('Latvian')),
    ('lt', _('Lithuanian')),
    ('lb', _('Luxembourgish')),
    ('mk', _('Macedonian')),
    ('mg', _('Malagasy')),
    ('ms', _('Malay')),
    ('ml', _('Malayalam')),
    ('mt', _('Maltese')),
    ('mi', _('Maori')),
    ('mr', _('Marathi')),
    ('mn', _('Mongolian')),
    ('my', _('Myanmar (Burmese)')),
    ('ne', _('Nepali')),
    ('no', _('Norwegian')),
    ('fa', _('Persian')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sm', _('Samoan')),
    ('sr', _('Serbian')),
    ('sn', _('Shona')),
    ('sd', _('Sindhi')),
    ('sk', _('Slovak')),
    ('sl', _('Slovenian')),
    ('so', _('Somali')),
    ('es', _('Spanish')),
    ('su', _('Sundanese')),
    ('sw', _('Swahili')),
    ('sv', _('Swedish')),
    ('tg', _('Tajik')),
    ('ta', _('Tamil')),
    ('te', _('Telugu')),
    ('th', _('Thai')),
    ('tr', _('Turkish')),
    ('uk', _('Ukrainian')),
    ('ur', _('Urdu')),
    ('uz', _('Uzbek')),
    ('vi', _('Vietnamese')),
    ('cy', _('Welsh')),
    ('xh', _('Xhosa')),
    ('yi', _('Yiddish')),
    ('yo', _('Yoruba')),
    ('zu', _('Zulu')),
)

APP_LANGUAGES = [x for x in LANGUAGES if x[0] in MODELTRANSLATION_LANGUAGES]
