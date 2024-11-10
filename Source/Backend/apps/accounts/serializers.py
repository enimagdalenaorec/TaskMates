from rest_framework import serializers 
class RegisterSerializer(serializers.Serializer): 
    username = serializers.CharField(max_length=255) 
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True, max_length=128) 
class LoginSerializer(serializers.Serializer): 
   email = serializers.EmailField() 
   password = serializers.CharField(write_only=True, max_length=128) 
