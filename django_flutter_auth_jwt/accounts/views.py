from django.shortcuts import render, redirect
from rest_framework.generics import GenericAPIView
from .serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswodSerializer,
    LogoutUserSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword, User
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse



# สร้าง view สำหรับการลงทะเบียน
class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    # สร้าง post method สำหรับการลงทะเบียน
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user["email"])
            print(user, "HI")
            return Response(
                {
                    "data": user,
                    "message": f"สวัสดี ขอบคุณ ที่ลงทะเบียน รหัสผ่านได้ถูกส่งไปยังบัญชีของคุณแล้ว",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# สร้าง view สำหรับการยืนยันผู้ใช้อีเมล
class UserVerifyEmailView(GenericAPIView):
    def post(self, request):
        otp_code = request.data.get("otp")
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response(
                    {"message": "ตรวจสอบบัญชีอีเมลเรียบร้อยแล้ว"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "รหัสไม่ถูกต้อง ผู้ใช้ได้ยืนยันตัวตนแล้ว"},
                status=status.HTTP_204_NO_CONTENT,
            )

        except OneTimePassword.DoesNotExist:
            return Response(
                {"message": "ไม่ได้ให้รหัสผ่านไว้"}, status=status.HTTP_404_NOT_FOUND
            )

# สร้าง view สำหรับการยืนยันผู้ใช้อีเมลอีกรูปแบบหนื่ง
def verify_email_code(request):
    one_time_password = OneTimePassword.objects.last()
    context = {"one_time_password": one_time_password}

    return render(request, "email/verify_email_code.html", context)


# สร้าง view สำหรับการเข้าสู่ระบบผู้ใช้
class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# สร้าง view สำหรับการตรวจสอบการเข้าสู่ระบบผู้ใช้
class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"msg": "Its works"}

        return Response(data, status=status.HTTP_200_OK)


# สร้าง view สำหรับการรีเซ็ตรหัสผ่าน
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # print(serializer)
        return Response(
            {"message": "ลิงก์ได้รับการส่งไปยังอีเมลของคุณเพื่อรีเซ็ตรหัสผ่านของคุณแล้ว"},
            status=status.HTTP_200_OK,
        )

# สร้าง view สำหรับการรีเซ็ตรหัสผ่านอีกรูปแบบหนื่ง
def password_reset_request(request, email):
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)  # Use get instead of filter to get the user object
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        site_domain = get_current_site(request).domain
        relative_link = reverse("password-reset-confirm-page", kwargs={"uidb64": uidb64, "token": token})

        abs_link = f"http://{site_domain}{relative_link}"

        context = {"abs_link": abs_link}

        return render(request, "email/password_reset_request.html", context)


# def password_reset_request(request):
#     if request.method == "POST":
#         form_data = request.POST
#         serializer = PasswordResetRequestSerializer(
#             data=form_data, context={"request": request}
#         )

#         if serializer.is_valid():
#             email = form_data.get("email")
#             if User.objects.filter(email=email).exists():
#                 user = User.objects.get(email=email)
#                 uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#                 token = PasswordResetTokenGenerator().make_token(user)

#                 site_domain = get_current_site(request).domain
#                 relative_link = reverse(
#                     "password-reset-confirm-page",
#                     kwargs={"uidb64": uidb64, "token": token},
#                 )
#                 abs_link = f"http://{site_domain}{relative_link}"

#                 text_content = (
#                     f"Hello, use the link below to reset your password:\n{abs_link}"
#                 )
#                 html_content = f"""
#                 <html>
#                     <body>
#                         <p>Hello,</p>
#                         <p>Please use the link below to reset your password:</p>
#                         <a href="{abs_link}">Reset Password</a>
#                         <p>If you did not request a password reset, please ignore this email.</p>
#                     </body>
#                 </html>
#                 """

#                 email_message = EmailMultiAlternatives(
#                     subject="Reset your password",
#                     body=text_content,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     to=[email],
#                 )
#                 email_message.attach_alternative(html_content, "text/html")
#                 email_message.send()
#                 # return redirect('pssword-reset-request-success')

#     # GET request or invalid form
#     return render(request, "email/password_reset_request.html")


# สร้าง view สำหรับการยืนยันการรีเซ็ตรหัสผ่าน
class PasswordResetConfirmView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"message": "โทเค็นไม่ถูกต้องหรือหมดอายุแล้ว"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {
                    "success": True,
                    "message": "ข้อมูลประจำตัวถูกต้อง",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )

        except DjangoUnicodeDecodeError:
            return Response(
                {"message": "โทเค็นไม่ถูกต้องหรือหมดอายุแล้ว"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# สร้าง view สำหรับการเปลี่ยนรหัสผ่าน
class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswodSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"message": "รีเซ็ตรหัสผ่านสำเร็จแล้ว"}, status=status.HTTP_200_OK)


# สร้าง view อกจากระบบผู้ใช้
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
