from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsAdmin, IsCandidate, ReadOnly
from rooms.models import Room
from scholarships import serializers
from scholarships.models import Scholarship


class ScholarshipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin | IsCandidate & ReadOnly]

    def get_queryset(self):
        qs = Scholarship.objects.all()

        if self.request.user.is_admin:
            qs = qs.filter(admin=self.request.user)

            if self.action == 'list':
                # If admin is listing, show analytics
                rooms_by_status = {
                    f'rooms_{status}': Count('rooms', filter=Q(rooms__status=status))
                    for status in Room.Status
                }
                qs = qs.annotate(**rooms_by_status)

            qs = qs.order_by('-is_active', '-created')

        else:
            qs = qs.filter(is_active=True)

        return qs

    def get_serializer_class(self):
        if self.request.user.is_candidate:
            return serializers.ScholarshipSimpleSerializer

        if self.action == 'list':
            return serializers.ScholarshipOverviewSerializer

        return serializers.ScholarshipSerializer

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
