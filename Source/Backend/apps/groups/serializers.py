from rest_framework import serializers 
class GroupSerializer(serializers.Serializer): 
   name = serializers.CharField(max_length=255) 
   image = serializers.CharField() 
class JoinGroupSerializer(serializers.Serializer): 
   code = serializers.CharField(max_length=10) 
