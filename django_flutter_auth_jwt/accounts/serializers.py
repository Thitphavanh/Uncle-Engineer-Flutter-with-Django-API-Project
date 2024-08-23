from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken
from tokenize import TokenError
from django.shortcuts import *


# สร้าง ลงทะเบียนผู้ใช้ Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        if password != password2:
            raise serializers.ValidationError("รหัสผ่านไม่ตรงกัน")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=validated_data.get("password"),
        )

        return user


# สร้าง เข้าสู่ระบบ Serializer
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "full_name", "access_token", "refresh_token"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("ข้อมูลประจำตัวไม่ถูกต้อง โปรดลองอีกครั้ง")
        # เพิ่มที่หลัง
        if not user.is_verified:
            raise AuthenticationFailed("อีเมล์ไม่ได้รับการตรวจสอบ")
        user_tokens = user.tokens()

        return {
            "email": user.email,
            "full_name": user.get_full_name,
            "access_token": str(user_tokens.get("access")),
            "refresh_token": str(user_tokens.get("refresh")),
        }


# สร้าง รีเซ็ตรหัสผ่าน Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get("request")
            site_domain = get_current_site(request).domain
            relative_link = reverse(
                "password-reset-confirm-page", kwargs={"uidb64": uidb64, "token": token}
            )

            abs_link = f"http://{site_domain}{relative_link}"

            email_body = f"สวัสดี ใช้ลิงก์ด้านล่างเพื่อรีเซ็ตรหัสผ่านของคุณ \n {abs_link}"

            data = {
                "email_body": email_body,
                "email_subject": "reset your password",
                "to_email": user.email,
            }

            print("data", data)
            send_normal_email(data)

        return super().validate(attrs)


# from django.contrib.auth import get_user_model
# User = get_user_model()

# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=255)

#     class Meta:
#         fields = ["email"]

#     def validate(self, attrs):
#         email = attrs.get("email")
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             request = self.context.get("request")
#             site_domain = get_current_site(request).domain
#             relative_link = reverse(
#                 "password-reset-confirm-page", kwargs={"uidb64": uidb64, "token": token}
#             )

#             abs_link = f"http://{site_domain}{relative_link}"

#             # Plain text content for non-HTML email clients
#             text_content = f"Hello,\nPlease use the link below to reset your password:\n{abs_link}"

#             # HTML content for email clients that support HTML
#             html_content = f"""
#             <html>
#                 <body>
#                     <p>Hello,</p>
#                     <p>Please use the link below to reset your password:</p>
#                     <a href="{abs_link}">Reset Password</a>
#                     <p>If you did not request a password reset, please ignore this email.</p>
#                 </body>
#             </html>
#             """

#             # Email subject
#             subject = "Reset your password"

#             # Prepare the email data
#             email_data = {
#                 "email_subject": subject,
#                 "email_body": text_content,
#                 "html_content": html_content,
#                 "to_email": user.email,
#             }

#             # Send the email
#             try:
#                 send_normal_email(email_data)
#             except Exception as e:
#                 # Log or handle the exception
#                 print(f"Error sending email: {e}")
#                 raise serializers.ValidationError("There was an error sending the email. Please try again later.")

#         return attrs


# สร้าง ตั้งรหัสผ่านใหม่ Serializer
class SetNewPasswodSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(
        max_length=100, min_length=6, write_only=True
    )
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"]

    def validate(self, attrs):
        try:
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            password = attrs.get("password")
            confirm_password = attrs.get("confirm_password")

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("ลิงค์รีเซ็ตไม่ถูกต้องหรือหมดอายุแล้ว", 401)
            if password != confirm_password:
                raise AuthenticationFailed("รหัสผ่านไม่ตรงกัน")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("ลิงค์ไม่ถูกต้องหรือหมดอายุแล้ว")


# สร้าง ออกจากระบบผู้ใช้ Serializer
class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {"bad_token": "โทเค็นไม่ถูกต้องหรือหมดอายุแล้ว"}

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:

            return self.fail("bad_token")
