from rest_framework import serializers
from .models import Tracker    

class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = "__all__"
        read_only_fields = ["block_hash", "created_at"]    