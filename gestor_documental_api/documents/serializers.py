from rest_framework import serializers
from .models import GeneratedDocument
class GeneratedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedDocument
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']
