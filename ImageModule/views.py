import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ImageModule.middleware.response_middleware import UnifiedResponseMiddleware
from ImageModule.models import Imagefile ,Videofile
from ImageModule.serializers import ImagefileSerializer,VideofileSerializer
from ImageModule.utils.crypt import EncryptedFileField
from airport_logistics_backend import settings
from .forms import ImageSearchForm, ImageUploadForm, VideoSearchForm, VideoUploadForm
from .utils import resjson
from rest_framework.response import Response
from cryptography.fernet import Fernet
import json
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import viewsets
from django.utils import timezone

def hello(request):
    return HttpResponse("Hello, world")   # 直接返回响应字符串
# Create your views here.

class ImageViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代ArticleList和ArticleDetail两个视图
    queryset = Imagefile.objects.all()
    serializer_class = ImagefileSerializer
    
    # POST 
    def create(self, request):
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
        return Response(serializer.data,status=200)   

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
    def create(self, request):
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
        return Response(serializer.data,status=200)   

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

    def list(self, request):
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




def upload_image(request):
    print('xxx')
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        json_str = request.body
        json_str = json_str.decode()  # python3.6 无需执行此步
        req_data = json.loads(json_str)
        print(req_data['uploadData'])
        if form.is_valid():
            Imagefile.objects.create(type = form.cleaned_data['type'],
                                     image = form.cleaned_data['image'],
                                     description = form.cleaned_data['description'],
                                     size = form.cleaned_data['image'].size)
            return HttpResponse("Image uploaded successfully")
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})

def search_image(request):
    images = None
    if 'search' in request.GET:
        form = ImageSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            upload_date = form.cleaned_data['date']
            type = form.cleaned_data['type']
            images = Imagefile.objects.all()
            if name:
                images = images.filter(name__icontains=name)
            if upload_date:
                images = images.filter(upload_date=upload_date)
            if type:
                images = images.filter(type=type)
        
        result  = resjson.resImageJson(images)

        return HttpResponse(result)
        
    else:
        form = ImageSearchForm()
    return render(request, 'search_image.html', {'form': form, 'image': images})

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






def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # video_instance = form.save(commit=False)
            # video_instance.name = request.FILES['video'].name  # 获取文件名作为视频名称
            # video_instance.size = request.FILES['video'].size
            # video_instance.user_id = request.environ['USER']    #后期需要修改
            # video_instance.save()
            Videofile.objects.create(video = form.cleaned_data['video'],
                                     description = form.cleaned_data['description'],
                                     size = form.cleaned_data['video'].size)

            return HttpResponse('Video uploaded successfully')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def search_video(request):
    videos = None
    if 'search' in request.GET:
        form = VideoSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data['name']
            upload_date = form.cleaned_data['upload_date']
            videos = Videofile.objects.all()
            if name:
                videos = videos.filter(name__icontains=name)
            if upload_date:
                videos = videos.filter(upload_date=upload_date)
    else:
        form = VideoSearchForm()
    return render(request, 'search_video.html', {'form': form, 'videos': videos})

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




def play_video(request, video_id):
    video = get_object_or_404(Videofile, pk=video_id)
    res = {
        "url"  : video.video.file.name
    }
    # return JsonResponse(res,safe=False)
    return render(request, 'play_video.html', {'video': video})


def show_all_videos(request):

    videos = Videofile.objects.all()

    model_data = []
    for item in videos:
        # delattr(item, 'video')
        item = {
            'id'    :   item.id,
            "name"  :   item.name,
            "data"  :   item.upload_date
        }
        model_data.append(item)
    result = { "data": model_data }
    return JsonResponse( result, safe=False )
    # form = VideoSearchForm(request.GET)
    # if form.is_valid():
    #     return JsonResponse({'success': True, 'data': form.cleaned_data})
    # # video = Video.objects.get(pk=video_id)
    # # video_url = request.build_absolute_uri(video.video.url)
    # # return render(request, 'show_all_videos.html', {'videos': videos})
    # return JsonResponse({'video_name': videos.name, 'video_url': videos.video})