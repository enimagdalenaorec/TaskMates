from rest_framework import serializers 
class AdminGroupSerializer(serializers.Serializer): 
   name = serializers.CharField(max_length=255) 
   image = serializers.CharField() 
class AdminDeleteGroupSerializer(serializers.Serializer): 
   groupId = serializers.CharField() 
