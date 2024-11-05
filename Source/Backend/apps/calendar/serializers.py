from rest_framework import serializers 
class CalendarTaskSerializer(serializers.Serializer): 
   icon = serializers.CharField(allow_null=True) 
   name = serializers.CharField(max_length=255) 
   id = serializers.CharField() 
