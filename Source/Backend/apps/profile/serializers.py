from rest_framework import serializers

class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class ChangeProfilePictureSerializer(serializers.Serializer):
    profilePicture = serializers.CharField(required=True)
