from rest_framework import serializers 
class TaskSerializer(serializers.Serializer): 
   id = serializers.CharField() 
   name = serializers.CharField(max_length=255) 
   icon = serializers.CharField(allow_null=True) 
   deadline = serializers.DateField(allow_null=True) 
   members = serializers.ListField(child=serializers.DictField(child=serializers.CharField())) 
class AddTaskSerializer(serializers.Serializer): 
   name = serializers.CharField(max_length=255) 
   icon = serializers.CharField(allow_null=True) 
   description = serializers.CharField() 
   maxCapacity = serializers.IntegerField() 
   date = serializers.DateField(allow_null=True) 
   timeOfDay = serializers.CharField(allow_null=True) 
   points = serializers.IntegerField() 
