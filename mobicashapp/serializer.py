from rest_framework import serializers
from .models import Project,Profile

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model =Project
        fields = ('sku', 'pname', 'description','link')
class MerchSerializerpro(serializers.ModelSerializer):
    class Meta:
        model =Profile
        fields = ('Name', 'bios', 'contact')