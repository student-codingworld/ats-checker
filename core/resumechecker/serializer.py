from rest_framework import serializers
from .models import JobDescription, Resume

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription   # ✅ Use the model class, not a string
        fields = '__all__'       # ✅ Keep this line as is

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Resume
        fields= '__all__'
