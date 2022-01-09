from rest_framework import serializers

from rooms.models import Document, Room
from scholarships.serializers import ScholarshipSimpleSerializer


class RoomSerializer(serializers.ModelSerializer):
    scholarship = ScholarshipSimpleSerializer()

    class Meta:
        model = Room

        fields = [
            'id',
            'scholarship',
            'status',
            'is_pinned',
            'unread_messages',
        ]


class DocumentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='requirement.name', read_only=True)

    class Meta:
        model = Document

        fields = [
            'id',
            'name',
            'content',
            'status',
            'review_comment',
            'reviewed_date',
        ]


class DocumentContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['content']

    def update(self, instance, validated_data):
        instance.upload(validated_data['content'])
        return instance
