from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

User = get_user_model()


class Scholarship(UUIDModel, TimeStampedModel, SoftDeletableModel):
    name = models.CharField(_('name'), max_length=255)

    description = models.TextField(_('description'), max_length=600, blank=True)

    admin = models.ForeignKey(User, verbose_name=_('admin'), null=True,
                              related_name='scholarships_created', on_delete=models.SET_NULL)

    evaluators = models.ManyToManyField(User, verbose_name=_('agents'),
                                        related_name='scholarships_assigned')

    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('scholarship')
        verbose_name_plural = _('scholarships')
