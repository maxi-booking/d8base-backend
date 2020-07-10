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

    # professional certificate
    'add_professionalcertificate',
    'change_professionalcertificate',
    'delete_professionalcertificate',

    # professional certificate
    'add_professionalphoto',
    'change_professionalphoto',
    'delete_professionalphoto',

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

    # message
    'change_message',
    'add_message',
    'delete_message',

    # suggested message
    'change_suggestedmessage',

    # review
    'change_review',
    'add_review',
    'delete_review',

    # review
    'change_reviewcomment',
    'add_reviewcomment',
    'delete_reviewcomment',

    # location
    'change_continent',
    'change_country',
    'change_region',
    'change_subregion',
    'change_city',
    'change_district',
    'change_postalcode',
    'change_alternativename',

    # rates
    'change_rate',

    # services
    'change_service',
    'add_service',
    'delete_service',

    # prices
    'change_price',
    'add_price',
    'delete_price',

    # serice tags
    'change_servicetag',
    'add_servicetag',
    'delete_servicetag',

    # serice locations
    'change_servicelocation',
    'add_servicelocation',
    'delete_servicelocation',

    # serice photos
    'change_servicephoto',
    'add_servicephoto',
    'delete_servicephoto',
]
