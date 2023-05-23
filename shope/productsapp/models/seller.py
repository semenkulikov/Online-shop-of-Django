from django.db import models

from coreapp.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Seller(BaseModel):
    """
    Класс-модель продавца
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("seller")
        verbose_name_plural = _("sellers")
