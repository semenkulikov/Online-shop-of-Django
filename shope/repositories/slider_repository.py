from interfaces import SliderInterface
from productsapp.models import Slider
from django.db.models import QuerySet


class SliderRepository(SliderInterface):

    def get_all(self) -> QuerySet[Slider]:
        return Slider.objects.all()
