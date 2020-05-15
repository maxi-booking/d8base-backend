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

    # user contacts
    'add_usercontact',
    'change_usercontact',
    'delete_usercontact',

    # user settings
    'add_usersettings',
    'change_usersettings',
    'delete_usersettings',

    # user saved professional
    'add_usersavedprofessional',
    'change_usersavedprofessional',
    'delete_usersavedprofessional',

    # professional
    'add_professional',
    'change_professional',
    'delete_professional',

    # professional tag
    'add_professionaltag',
    'change_professionaltag',
    'delete_professionaltag',

    # professional contacts
    'add_professionalcontact',
    'change_professionalcontact',
    'delete_professionalcontact',

    # professional education
    'add_professionaleducation',
    'change_professionaleducation',
    'delete_professionaleducation',

    # professional experience
    'add_professionalexperience',
    'change_professionalexperience',
    'delete_professionalexperience',

    # professional locations
    'add_professionallocation',
    'change_professionallocation',
    'delete_professionallocation',

    # contact
    'change_contact',

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
