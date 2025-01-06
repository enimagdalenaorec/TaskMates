from rest_framework import serializers

class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class ChangeProfilePictureSerializer(serializers.Serializer):
    # Ako biste slali base64 string slike ili sl.
    # Ili eventualno serializers.ImageField() ako radite s file uploadom
    profilePicture = serializers.CharField(required=True)
