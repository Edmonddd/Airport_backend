from rest_framework import serializers
from .models import Imagefile, Videofile
from django.contrib.auth import get_user_model

User = get_user_model()

class ImagefileSerializer(serializers.ModelSerializer):
    # 这是一个可选字段
    name = serializers.CharField(required=False)

    class Meta:
        model = Imagefile
        fields = '__all__'
        read_only_fields = ['upload_date']

class VideofileSerializer(serializers.ModelSerializer):
    # 这是一个可选字段
    name = serializers.CharField(required=False)
    # upload_date = serializers.DateTimeField(required=False,format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Videofile
        fields = '__all__'
        read_only_fields = ['upload_date']
         