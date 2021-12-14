from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.managers import SoftDeletableManager
from model_utils.models import TimeStampedModel, SoftDeletableModel

User = get_user_model()


class Loan(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(_('name'), max_length=50)

    user = models.ForeignKey(User, verbose_name=_('user'), related_name='loans', on_delete=models.CASCADE)

    amount = models.FloatField(_('amount'), validators=[MinValueValidator(0.0)])

    term = models.PositiveIntegerField(_('term in years'), validators=[MinValueValidator(1)])

    down_payment = models.FloatField(_('down payment'), validators=[MinValueValidator(0.0)])

    objects = models.Manager()
    available_objects = SoftDeletableManager()

    class Meta:
        verbose_name = _('loan')
        verbose_name_plural = _('loans')
