"""The messenger settings module."""

EMAIL_SUBJECT_PREFIX = 'd8b: '

D8B_MESSENGER_TASKS = [
    'communication.notifications.tasks.send_email',
    'communication.notifications.tasks.send_push',
]
