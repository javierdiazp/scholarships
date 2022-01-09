from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from scholarships.models import Scholarship

User = get_user_model()


class Room(UUIDModel, TimeStampedModel, SoftDeletableModel):
    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', _('In progress')
        LOST = 'lost', _('Lost')
        WON = 'won', _('Won')

    scholarship = models.ForeignKey(Scholarship, verbose_name=_('scholarship'),
                                    related_name='rooms', on_delete=models.CASCADE)

    candidate = models.ForeignKey(User, verbose_name=_('candidate'),
                                  related_name='rooms_applying', on_delete=models.CASCADE)

    evaluator = models.ForeignKey(User, verbose_name=_('evaluator'),
                                  related_name='rooms_assigned', on_delete=models.CASCADE)

    status = models.CharField(_('status'), max_length=20, choices=Status.choices, default=Status.IN_PROGRESS)

    is_active = models.BooleanField(_('active'), default=True)

    is_pinned = models.BooleanField(_('pinned'), default=False)

    unread_messages = models.PositiveIntegerField(_('unread messages'), default=0)

    class Meta:
        verbose_name = _('room')
        verbose_name_plural = _('rooms')


class Message(TimeStampedModel):
    room = models.ForeignKey(Room, verbose_name=_('room'), related_name='messages', on_delete=models.CASCADE)

    author = models.ForeignKey(User, verbose_name=_('author'), related_name='messages', on_delete=models.CASCADE)

    content = models.TextField(_('message content'), max_length=500)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def as_json(self):
        return {
            'author': str(self.author),
            'content': self.content,
            'timestamp': str(self.created)
        }


class StatusLog(TimeStampedModel):
    room = models.ForeignKey(Room, verbose_name=_('room'), related_name='status_logs', on_delete=models.CASCADE)

    status = models.CharField(_('status'), max_length=20, choices=Room.Status.choices)

    class Meta:
        verbose_name = _('status log')
        verbose_name_plural = _('status logs')
