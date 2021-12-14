from django.core.validators import MinValueValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

from loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    purchase_price = serializers.FloatField(label=_('purchase price'), validators=[MinValueValidator(0.0)])

    class Meta:
        model = Loan

        fields = [
            'id',
            'name',
            'amount',
            'term',
            'purchase_price',
            'down_payment',
        ]

        read_only_fields = ['amount']

    def validate(self, attrs):
        purchase_price = attrs['purchase_price']
        down_payment = attrs['down_payment']

        if down_payment > purchase_price:
            raise serializers.ValidationError({'down_payment': _('Down payment cannot be greater than price')})

        attrs['amount'] = attrs['purchase_price'] - attrs['down_payment']

        return attrs
