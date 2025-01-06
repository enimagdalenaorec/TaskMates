from rest_framework import serializers

class GetTaskByIdSerializer(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)

class GetTasksByGroupSerializer(serializers.Serializer):
    groupId = serializers.IntegerField(required=True)

class AddTaskSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    deadline = serializers.CharField(required=True)
    groupId = serializers.IntegerField(required=True)
    icon = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    max_capacity = serializers.IntegerField(required=False, default=1)
    description = serializers.CharField(required=False, allow_blank=True, default='')
    points = serializers.IntegerField(required=False, default=100)

class JoinTaskSerializer(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)

class LeaveTaskSerializer(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)

class FinishTaskSerializer(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)

class ReviewTaskSerializer(serializers.Serializer):
    taskId = serializers.IntegerField(required=True)
    value = serializers.IntegerField(required=True, min_value=1, max_value=5)
