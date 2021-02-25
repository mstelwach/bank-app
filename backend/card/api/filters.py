from django_filters.rest_framework import FilterSet

from card.models import Card


class CardFilter(FilterSet):
    class Meta:
        model = Card
        fields = ('is_active', )

