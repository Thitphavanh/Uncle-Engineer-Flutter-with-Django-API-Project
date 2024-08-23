import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings


# function to generate otp
def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))

    return otp


# function ส่งรหัส OTP ไปยังอีเมล์ผู้ใช้งาน
def send_code_to_user(email):
    Subject = "รหัสผ่านครั้งเดียวสำหรับการยืนยันอีเมล"
    otp_code = generateOTP()
    print(otp_code, "HI")
    user = User.objects.get(email=email)
    current_site = "black-white.com"
    email_body = f"สวัสดี {user.first_name} ขอบคุณที่ลงทะเบียน {current_site} กรุณายืนยันที่อยู่อีเมลของคุณ \n ด้วยรหัสผ่านครั้งเดียว {otp_code}"

    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)

    direct_email = EmailMessage(
        subject=Subject, body=email_body, from_email=from_email, to=[email]
    )
    direct_email.send(fail_silently=True)


# function ในการส่งอีเมล์ถึงผู้ใช้งาน
def send_normal_email(data):
    email = EmailMessage(
        subject=data["email_subject"],
        body=data["email_body"],
        from_email=settings.EMAIL_HOST_USER,
        to=[data["to_email"]],
    )

    email.send()

