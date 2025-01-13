from rest_framework import serializers

class JoinGroupSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)

class CreateGroupSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    image = serializers.CharField(required=False)

class GetAllMembersSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)

class GetGroupCodeSerializer(serializers.Serializer):
    group_id = serializers.IntegerField(required=True)

class LeaveGroupSerializer(serializers.Serializer):
    groupId = serializers.IntegerField()