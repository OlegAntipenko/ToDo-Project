from rest_framework import serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    short_text = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = (
            'title',
            'short_text',
            'deadline',
            'status'
        )

    def get_short_text(self, obj):
        return obj.text[:250]

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'title',
            'text',
            'deadline',
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = (
            'status',
        )
