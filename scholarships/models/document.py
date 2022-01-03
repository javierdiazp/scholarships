from django.db import models
from django.utils.text import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from scholarships.models.scholarship import Scholarship


class RequiredDocument(UUIDModel, TimeStampedModel, SoftDeletableModel):
    scholarship = models.ForeignKey(Scholarship, verbose_name=_('scholarship'),
                                    related_name='required_documents', on_delete=models.CASCADE)

    name = models.CharField(_('name'), max_length=50)

    description = models.TextField(_('description'), max_length=300)

    attachment = models.FileField(_('file'), upload_to='attachments', blank=True)

    class Meta:
        verbose_name = _('required document')
        verbose_name_plural = _('required documents')
