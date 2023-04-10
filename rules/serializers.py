from rest_framework import serializers
from rules.models import Rules


class RulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rules
        fields = ['id', 'rules', 'status']
