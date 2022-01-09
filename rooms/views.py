from django.http import FileResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsCandidate, IsEvaluator
from rooms import serializers
from rooms.models import Document, Room


class RoomListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsEvaluator | IsCandidate]
    serializer_class = serializers.RoomSerializer

    def get_queryset(self):
        qs = Room.objects.all()

        if self.request.user.is_evaluator:
            qs = qs.filter(evaluator=self.request.user)
        else:
            qs = qs.filter(candidate=self.request.user)

        return qs


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEvaluator | IsCandidate]
    serializer_class = serializers.DocumentSerializer

    def get_queryset(self):
        qs = Document.objects.select_related('requirement').filter(room_id=self.kwargs['room_id'])

        if self.request.user.is_evaluator:
            qs = qs.filter(room__evaluator=self.request.user)
        else:
            qs = qs.filter(room__candidate=self.request.user)

        return qs

    @action(detail=True, methods=['put'], serializer_class=serializers.DocumentContentSerializer)
    def content(self, request, *args, **kwargs):
        """ Upload content to the document """
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @content.mapping.get
    def download_content(self, request, *args, **kwargs):
        """ Download content from the document """
        instance = self.get_object()
        file = instance.content
        return FileResponse(file, filename=file.name, as_attachment=True)

    @action(detail=True, methods=['get'])
    def attachment(self, request, *args, **kwargs):
        """ Download attachment from the requirement """
        instance = self.get_object()
        file = instance.requirement.attachment
        return FileResponse(file, filename=file.name, as_attachment=True)
