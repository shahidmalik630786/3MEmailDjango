from .models import TemplateModel, EmailModel
from rest_framework import serializers


class TemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = TemplateModel
        fields = ['name', "subject", "body", "file"]

    def validate_name(self, value):
        if TemplateModel.objects.filter(name=value).exists():
            raise serializers.ValidationError("Template name already exists")
        return value
    

class TemplateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateModel
        fields = ['name', "subject", "body", "file"]


class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailModel
        fields = ["template", "to", "name", "date", "time"]