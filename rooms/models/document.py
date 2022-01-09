from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from rooms.models.room import Room
from scholarships.models import RequiredDocument

User = get_user_model()


class Document(UUIDModel, TimeStampedModel, SoftDeletableModel):
    class Status(models.TextChoices):
        NONE = 'none', _('Not uploaded')
        UPLOADED = 'uploaded', _('Uploaded')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')

    room = models.ForeignKey(Room, verbose_name=_('campaign'),
                             related_name='documents', on_delete=models.CASCADE)

    requirement = models.ForeignKey(RequiredDocument, verbose_name=_('requirement'),
                                    related_name='documents', on_delete=models.CASCADE)

    content = models.FileField(_('content'), upload_to='documents', blank=True)

    status = models.CharField(_('status'), max_length=20, choices=Status.choices, default=Status.NONE)

    review_comment = models.TextField(_('review'), max_length=400, blank=True)

    reviewed_by = models.ForeignKey(User, verbose_name=_('reviewed by'),
                                    related_name='reviewed_documents',
                                    blank=True, null=True,
                                    on_delete=models.SET_NULL)

    reviewed_date = models.DateTimeField(_('reviewed date'), blank=True, null=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def upload(self, file):
        if self.room.status != self.room.Status.IN_PROGRESS:
            raise ValidationError(_('Cannot upload a document if the room is not in progress'))

        if self.status == self.Status.APPROVED:
            raise ValidationError(_('Cannot overwrite an approved document'))

        ext = file.name.split('.')[-1]
        file.name = f'{slugify(self.requirement.name)}.{ext}'

        self.content = file
        self.status = self.Status.UPLOADED

        self.review_comment = ''
        self.reviewed_by = None
        self.reviewed_date = None

        self.save()
