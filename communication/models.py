"""The communication models module."""
from typing import Any, Callable, Dict, List

from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from d8b.fields import RatingField
from d8b.models import CommonInfo, ValidationMixin
from users.models import User

from .managers import (AbstractRemindersManager, MessageManager,
                       ReviewCommentManager, ReviewManager,
                       SuggestedMessageManager)
from .services import (notify_new_message, notify_new_review,
                       notify_new_review_comment)
from .validators import (validate_message_parent, validate_message_recipient,
                         validate_reminder_remind_before,
                         validate_review_comment_user, validate_review_user)


class AbstractReminder(CommonInfo, ValidationMixin):
    """The abstract reminder class."""

    subject: str = ""
    template: str = ""
    validators: List[Callable[["AbstractReminder"], None]] = []

    objects: AbstractRemindersManager = AbstractRemindersManager()

    remind_before = models.PositiveIntegerField(
        _("remind"),
        help_text=_("number of minutes for a reminder before the event"),
        db_index=True,
        validators=[validate_reminder_remind_before],
    )
    remind_before_datetime = models.DateTimeField(
        verbose_name=_("remind before datetime"),
        db_index=True,
        editable=False,
    )
    is_reminded = models.BooleanField(
        default=False,
        verbose_name=_("is reminded?"),
        db_index=True,
        editable=False,
    )
    recipient: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_reminders",
        verbose_name=_("recipient"),
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"reminder #{self.pk}: {self.recipient}"

    def get_data(self) -> Dict[str, Any]:
        """Return the data."""
        raise NotImplementedError()

    def set_remind_before_datetime(self):
        """Set the remind_before_datetime field."""
        raise NotImplementedError()

    def save(self, **kwargs):
        """Save the object."""
        self.set_remind_before_datetime()
        super().save(**kwargs)

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = True


class SuggestedMessage(CommonInfo):
    """The suggestion class."""

    objects = SuggestedMessageManager()

    subcategory = models.ForeignKey(
        "professionals.Subcategory",
        on_delete=models.SET_NULL,
        related_name="suggested_answers",
        verbose_name=_("subcategory"),
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("name"),
        max_length=255,
        db_index=True,
    )
    body = models.TextField(_("body"))
    is_enabled = models.BooleanField(
        default=True,
        verbose_name=_("is enabled?"),
        db_index=True,
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.name}"


class Review(CommonInfo, ValidationMixin):
    """The review class."""

    validators = [validate_review_user]
    notifier: Callable[["Review"], None] = notify_new_review
    objects = ReviewManager()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("user"),
    )
    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("professional"),
    )
    title = models.CharField(
        _("title"),
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )
    description = models.TextField(
        _("description"),
        db_index=True,
        validators=[MinLengthValidator(settings.D8B_REVIEW_MIN_LENGTH)],
    )
    rating: int = RatingField()

    def save(self, **kwargs):
        """Save the object."""
        self.notifier()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.user}->{self.professional}: review {self.title}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False
        unique_together = (("user", "professional"), )


class ReviewComment(CommonInfo, ValidationMixin):
    """The review comment class."""

    validators = [validate_review_comment_user]
    notifier: Callable[["Review"], None] = notify_new_review_comment
    objects = ReviewCommentManager()

    review = models.OneToOneField(
        Review,
        on_delete=models.CASCADE,
        related_name="comment",
        unique=True,
        verbose_name=_("review"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="review_comments",
        verbose_name=_("user"),
    )
    title = models.CharField(
        _("title"),
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )
    description = models.TextField(
        _("description"),
        db_index=True,
        validators=[MinLengthValidator(settings.D8B_REVIEW_MIN_LENGTH)],
    )

    def __str__(self) -> str:
        """Return the string representation."""
        return f"Comment to the {self.review}"

    def save(self, **kwargs):
        """Save the object."""
        self.notifier()
        super().save(**kwargs)

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False


class Message(CommonInfo, ValidationMixin):
    """The message class."""

    validators = [validate_message_recipient, validate_message_parent]
    notifier: Callable[["Review"], None] = notify_new_message
    objects = MessageManager()

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("sender"),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name=_("recipient"),
    )
    subject = models.CharField(
        _("subject"),
        max_length=255,
        blank=True,
        null=True,
        db_index=True,
    )
    body = models.TextField(_("body"))
    is_read = models.BooleanField(
        default=False,
        editable=False,
        help_text=_("Has the message been read?"),
        verbose_name=_("is read?"),
        db_index=True,
    )
    read_datetime = models.DateTimeField(
        _("read date"),
        blank=True,
        null=True,
        editable=False,
    )
    is_deleted_from_sender = models.BooleanField(
        default=False,
        editable=False,
        help_text=_("Has the message been deleted from sender?"),
        verbose_name=_("is deleted from sender?"),
        db_index=True,
    )
    delete_from_sender_datetime = models.DateTimeField(
        _("delete from sender datetime "),
        blank=True,
        null=True,
        editable=False,
    )
    is_deleted_from_recipient = models.BooleanField(
        default=False,
        editable=False,
        help_text=_("Has the message been deleted from recipient?"),
        verbose_name=_("is deleted from recipient?"),
        db_index=True,
    )
    delete_from_recipient_datetime = models.DateTimeField(
        _("delete from recipient datetime "),
        blank=True,
        null=True,
        editable=False,
    )

    def save(self, **kwargs):
        """Save the object."""
        self.notifier()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.sender}->{self.recipient}: {self.subject}"

    class Meta(CommonInfo.Meta):
        """The metainformation."""

        abstract = False
