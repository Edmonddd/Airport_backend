from cryptography.fernet import Fernet
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response

from ImageModule.models import Imagefile, Videofile
from ImageModule.serializers import ImagefileSerializer, VideofileSerializer
from ImageModule.utils.crypt import EncryptedFileField
from airport_logistics_backend import settings


# Create your views here.

class ImageViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代ArticleList和ArticleDetail两个视图
    queryset = Imagefile.objects.all()
    serializer_class = ImagefileSerializer

    # POST 
    def create(self, request, **kwargs):
        serializer = ImagefileSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            # custom_response = {'data': ImagefileSerializer(instance).data, 'message': 'Custom create response'}
            a = ImagefileSerializer(instance)
            # return Response(ImagefileSerializer(instance).data)
            return Response({'message': '新建图片成功'}, status=201)
        return Response(serializer.errors, status=400)

    # GET
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self):
        queryset = Imagefile.objects.all()
        name = self.request.query_params.get('name')
        date = self.request.query_params.get('date')
        type = self.request.query_params.get('type')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if date:
            queryset = queryset.filter(date=date)
        if type:
            queryset = queryset.filter(type__icontains=type)

        return queryset


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Videofile.objects.all()
    serializer_class = VideofileSerializer

    # POST 
    def create(self, request, **kwargs):
        uploadData = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        request.data['upload_date'] = uploadData
        serializer = VideofileSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            # custom_response = {'data': ImagefileSerializer(instance).data, 'message': 'Custom create response'}
            # return Response(ImagefileSerializer(instance).data)
            return Response({'message': '新建视频成功'}, status=201)
        return Response(serializer.errors, status=400)

    # GET
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self):
        queryset = Videofile.objects.all()
        name = self.request.query_params.get('name')
        startDate = self.request.query_params.get('startDate')
        endDate = self.request.query_params.get('endDate')
        # date = date.split('T')[0]

        if name:
            queryset = queryset.filter(name__icontains=name)
        if startDate:
            queryset = queryset.filter(upload_date__gte=startDate)
            queryset = queryset.filter(upload_date__lt=endDate)

        return queryset


class ImageDownloadViewSet(viewsets.ModelViewSet):
    queryset = Imagefile.objects.all()
    serializer_class = ImagefileSerializer

    def list(self, request, **kwargs):
        cipher_suite = Fernet(EncryptedFileField.get_encryption_key())

        encrypted_file_path = request.GET['url']
        encrypted_file_path = settings.MEDIA_ROOT + '/' + encrypted_file_path
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_content = encrypted_file.read()
            decrypted_content = cipher_suite.decrypt(encrypted_content)
        # 设置响应头
        response = HttpResponse(content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="image.png"'

        # 设置响应内容
        response.write(decrypted_content)

        return Response()


def download_image(request):
    cipher_suite = Fernet(EncryptedFileField.get_encryption_key())

    encrypted_file_path = request.GET['url']
    encrypted_file_path = settings.MEDIA_ROOT + '/' + encrypted_file_path
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_content = encrypted_file.read()
        decrypted_content = cipher_suite.decrypt(encrypted_content)

    # 设置响应头
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="image.png"'

    # 设置响应内容
    response.write(decrypted_content)

    return response


def download_video(request):
    cipher_suite = Fernet(EncryptedFileField.get_encryption_key())

    encrypted_file_path = request.GET['url']
    encrypted_file_path = encrypted_file_path.split('mediatest/')[1]
    encrypted_file_path = settings.MEDIA_ROOT + '/' + encrypted_file_path
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_content = encrypted_file.read()
        decrypted_content = cipher_suite.decrypt(encrypted_content)

    # 设置响应头
    response = HttpResponse(content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename="video.mp4"'

    # 设置响应内容
    response.write(decrypted_content)

    return response
    # return Response(decrypted_content, content_type='video/mp4', status=200)
