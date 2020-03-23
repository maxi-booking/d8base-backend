"""The language settings module."""
from typing import List

GROUP_USER_NAME: str = 'user'

GROUP_USER_PERMISSIONS: List[str] = [
    # user languages
    'add_userlanguage',
    'change_userlanguage',
    'delete_userlanguage',

    # user locations
    'add_userlocation',
    'change_userlocation',
    'delete_userlocation',

    # location
    'change_continent',
    'change_country',
    'change_region',
    'change_subregion',
    'change_city',
    'change_district',
    'change_postalcode',
    'change_alternativename',
]
