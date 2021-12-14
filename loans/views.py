from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from config.settings import MAX_LOANS_PER_USER
from loans.models import Loan
from loans.serializers import LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.available_objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.get_queryset().count() < MAX_LOANS_PER_USER:
            instance = serializer.save(user=self.request.user)
        else:
            raise ValidationError(_('You have reached the limit of allowed loans'))

        # TODO Generate opportunities
