import datetime
from django.db import models
from django.contrib.auth.models import User
from .utils import crypt

def images_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/{0}/{1}'.format(str(datetime.date.today()), filename)

def videos_user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'videos/{0}/{1}'.format(str(datetime.date.today()), filename)
    
# 设置对象结构（对应数据库的结构）
class Imagefile(models.Model):
    name = models.CharField(max_length=200)  # 字符串类型字段
    image = crypt.EncryptedFileField(upload_to=images_user_directory_path)
    # image = models.ImageField(upload_to=images_user_directory_path)
    type = models.PositiveIntegerField(default=0)  # 整数类型字段,null=True允许为空
    description = models.TextField(blank=True, null=True)
    size = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)  # 时间类型字段，参数为人类可读的字段名
    path = models.CharField(max_length=200,null=True)

    # 模型的元数据Meta
    class Meta:  # 注意，是模型的子类，要缩进！
        db_table = 'imagefile'
        ordering = ['-upload_date']

# 视频数据结构
class Videofile(models.Model):
    name = models.CharField(max_length=255)
    video = crypt.EncryptedFileField(upload_to=videos_user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    user = models.CharField(max_length=50,default='')
    status = models.CharField(max_length=50,default='')

    # def __str__(self):
    #     return self.name

    # 模型的元数据Meta
    class Meta:  # 注意，是模型的子类，要缩进！
        db_table = 'videofile'
    

