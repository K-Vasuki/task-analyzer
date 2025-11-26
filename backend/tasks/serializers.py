# backend/tasks/serializers.py
from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)  # optional id from input
    title = serializers.CharField()
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(required=False, default=1.0)
    importance = serializers.IntegerField(required=False, default=5)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False, default=list)

class TaskOutputSerializer(TaskInputSerializer):
    score = serializers.FloatField()
    reason = serializers.CharField()
