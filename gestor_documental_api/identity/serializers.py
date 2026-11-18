from rest_framework import serializers
from .models import InstitutionalIdentity
class InstitutionalIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalIdentity
        fields = '__all__'
