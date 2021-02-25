from rest_framework.serializers import ModelSerializer

from card.models import Card


class CardSerializer(ModelSerializer):

    class Meta:
        model = Card
        fields = ('pk', 'account', 'is_active', 'number', 'expires_date', 'code', 'pin')
