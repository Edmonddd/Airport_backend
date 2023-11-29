from django.urls import path

from . import views
from .views import download_image, download_video

app_name = 'app1_name'  # 关键是这行，这样对不同app下相同名称的url就可以进行区分了。{% url 'app1:inserpath' %}

image_upload = views.ImageViewSet.as_view(
    {
        'post': 'create',
        'get': 'list'
    })

video_upload = views.VideoViewSet.as_view(
    {
        'post': 'create',
        'get': 'list'
    })

urlpatterns = [
    # url(r'^$', views.index, name='index'),  # ^$正则表示为空，ex:http://127.0.0.1:8000/app1/
    # url(r'^insert/', views.insertuser,name='inserpath'),  # 直接映射到函数
    # url(r'^alluser/', views.findalluser,name='alluserpath'),  # 直接映射到函数
    # url(r'^finduser/', views.finduser),  # 直接映射到函数
    # # url通过(?P<name>pattern)来接收参数。因此(?P<userid>[0-9]+)就是一个参数。重定向到这个url时需要传递这个参数，url才能完整生成。
    # # ex:reverse('app1_name:detail', args=11) 生成网址/app1/11/detail/
    # url(r'^(?P<userid>[0-9]+)/detail/$', views.detail, name='detail'),
    # path('userid/<int:userid>/', views.detail),
    # # 重定向
    path('downloadimage/', download_image, name='download_image'),
    path('downloadvideo/', download_video, name='download_video'),

    path('uploadimage2/', image_upload),
    path('uploadvideo2/', video_upload),
]
