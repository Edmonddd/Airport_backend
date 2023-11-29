from cryptography.fernet import Fernet
from django.db import models
from django.core.files.base import ContentFile
import os

# 生成密钥，实际应用中应该保存这个密钥
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)

# def encrypt_image(image_data):
#     return cipher_suite.encrypt(image_data)

# def decrypt_image(encrypted_data):
#     return cipher_suite.decrypt(encrypted_data)

class EncryptedFileField(models.FileField):
    # fernet_key = Fernet.generate_key()
    fernet_key = b'GyPq_tY3W9ldTG5Ln7cNrKI9EPf6GjQisssCk0qXyM0='
    cipher_suite = Fernet(fernet_key)

    def __init__(self, *args, **kwargs):
        # self.fernet_key = fernet_key
        # self.cipher_suite = cipher_suite
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = getattr(model_instance, self.attname)

        # 只在文件对象存在且未提交时处理
        if file and not file._committed:
            # 读取文件内容
            content = file.read()

            # 加密文件内容
            encrypted_content = self.cipher_suite.encrypt(content)

            # 创建加密文件的内容对象
            encrypted_file = ContentFile(encrypted_content)

            # 保存加密文件
            # file_name = self.generate_filename(model_instance, os.path.basename(file.name))
            if hasattr(model_instance,'image'):
                file_name = model_instance.image.name
            elif hasattr(model_instance,'video'):
                file_name = model_instance.video.name

            file.save(file_name, encrypted_file, save=False)

        return super().pre_save(model_instance, add)
    
    # def pre_save(self, model_instance, add):
    #     # file_field = super().pre_save(model_instance, add)
    #     file_field = getattr(model_instance, self.attname)
    #     if file_field and file_field.file and not file_field._committed:
    #         # 加密文件内容
    #         content = file_field.file.read()
    #         encrypted_content = self.cipher_suite.encrypt(content)

    #         # 保存加密文件到临时位置
    #         temp_file_path = file_field.file.temporary_file_path()
    #         with open(temp_file_path, 'wb') as encrypted_file:
    #             encrypted_file.write(encrypted_content)
    #     file_field = super().pre_save(model_instance, add)
    #     return file_field
    # def __init__(self, *args, **kwargs):
    #     self.fernet_key = Fernet.generate_key()
    #     self.cipher_suite = Fernet(self.fernet_key)
    #     super().__init__(*args, **kwargs)


    # def save_form_data(self, instance, data):
    #     # 检查是否有新文件上传
        
    #     if data and hasattr(data, 'read'):
    #         # 加密文件内容
    #         original_file_content = data.read()
    #         encrypted_content = self.cipher_suite.encrypt(original_file_content)

    #         # 创建加密文件的内容对象
    #         encrypted_file = ContentFile(encrypted_content)

    #         # 更新实例属性
    #         # setattr(instance, self.name, encrypted_file)

    #     super().save_form_data(instance, encrypted_file)

    def get_encryption_key():
        return EncryptedFileField.fernet_key