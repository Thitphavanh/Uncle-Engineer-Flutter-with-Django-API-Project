from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken


# create class user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email Address")
    )
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    '''
    USERNAME_FIELD ใน Django คือการตั้งค่าที่ใช้กำหนดฟิลด์ของโมเดลที่ใช้เป็นชื่อผู้ใช้ (username)
    สำหรับการล็อกอินเข้าระบบ โดยปกติแล้ว ฟิลด์นี้จะถูกตั้งเป็น username ในโมเดล User เริ่มต้นของ 
    Django แต่ถ้าคุณใช้ฟิลด์อื่นแทน เช่น email คุณสามารถตั้งค่า USERNAME_FIELD ในคลาสโมเดลที่คุณกำหนดเองได้
    '''
    USERNAME_FIELD = "email"

    '''
    ในตัวอย่างนี้ REQUIRED_FIELDS ประกอบด้วย first_name และ last_name ซึ่งหมายความว่าเมื่อคุณสร้างผู้ใช้ใหม่
    คุณต้องระบุค่าฟิลด์เหล่านี้ร่วมกับฟิลด์ที่กำหนดใน USERNAME_FIELD (ในที่นี้คือ email) หมายเหตุ: ฟิลด์ที่อยู่ใน 
    REQUIRED_FIELDS ไม่ต้องรวมฟิลด์ที่เป็น USERNAME_FIELD และฟิลด์ password
    '''
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

     

class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"
