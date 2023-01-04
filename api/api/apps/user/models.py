from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """
    小区住户模型
    """

    stated = models.CharField(max_length=16, blank=True, verbose_name="用户身份码")
    rom_num = models.CharField(max_length=16, null=True, verbose_name="房号")
    car_num = models.CharField(max_length=32, null=True, verbose_name="车牌号")
    build_num = models.CharField(max_length=8, null=True, verbose_name="所在楼栋")
    uni_num = models.CharField(max_length=64, blank=True, verbose_name="住房所在楼栋的单元")
    sex = models.CharField(max_length=8, null=True, verbose_name="性别")
    mobile = models.CharField(max_length=16, unique=True, null=True, verbose_name="用户手机号")
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="用户头像")

    class Meta:
        db_table = "village_user"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
