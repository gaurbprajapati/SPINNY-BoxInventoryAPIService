from rest_framework import serializers
from .models import Box


class BoxSerializer(serializers.ModelSerializer):
    # Use StringRelatedField to show the username
    creator = serializers.StringRelatedField()

    class Meta:
        model = Box
        fields = '__all__'  # Include all fields, including 'creator'
