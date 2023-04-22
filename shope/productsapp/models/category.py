from django.db import models
from coreapp.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100,
                            null=False,
                            blank=True,
                            verbose_name="name")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name
