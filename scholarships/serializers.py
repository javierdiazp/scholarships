from django.contrib.auth import get_user_model
from rest_framework import serializers

from scholarships.models import RequiredDocument, Scholarship

User = get_user_model()


class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument

        fields = [
            'id',
            'name',
            'description',
            'attachment',
        ]


class ScholarshipSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(slug_field='email', read_only=True)

    evaluators = serializers.SlugRelatedField(queryset=User.objects.filter(is_evaluator=True),
                                              slug_field='email', many=True)

    class Meta:
        model = Scholarship

        fields = [
            'id',
            'name',
            'description',
            'admin',
            'evaluators',
            'is_active',
            'created',
        ]

    def update(self, instance, validated_data):
        if 'is_active' in validated_data:
            instance.is_active = validated_data['is_active']
            instance.save()

        if 'evaluators' in validated_data:
            instance.evaluators.add(*validated_data['evaluators'])

        return instance


class ScholarshipSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship

        fields = [
            'id',
            'name',
            'description',
        ]


class ScholarshipOverviewSerializer(serializers.ModelSerializer):
    rooms_in_progress = serializers.IntegerField()
    rooms_won = serializers.IntegerField()
    rooms_lost = serializers.IntegerField()

    class Meta:
        model = Scholarship

        fields = [
            'id',
            'name',
            'rooms_in_progress',
            'rooms_won',
            'rooms_lost',
        ]
