from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers

from .decorators import admin_api, all_api, buyer_api, seller_api

from .services import encodeOTP, google_validation, sendEmail, user_get, user_get_all, user_get_me, jwt_login, user_delete, user_get_create, create_buyer, update_buyer, get_buyer, verifyOTP

# Create your views here.

class UserAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        google_id = serializers.CharField(max_length=50)
    def post(self,request,*args,**kwargs):
        id_token = request.headers['Authorization']
        google_validation(id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user, registered = user_get_create(data['email'],data['google_id'])
            
        response = Response(data=user_get_me(user, registered))

        response, token = jwt_login(response,user)

        user_data = user_get_me(user, registered)
        data_response = {
            "id":user_data['id'],
            "google_id":user_data['google_id'],
            "user_type":user_data['user_type'],
            "registered":user_data['registered'],
            "token":token
        }
        response = Response(data=data_response)
        return response
    
    def delete(self,request,*args,**kwargs):
        data = request.GET['google_id']
        user_delete(google_id=data)
        return Response(status=status.HTTP_200_OK)

class UsersAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request,*args,**kwargs):
        response={"users":user_get_all()}
        return Response(data=response)

class BuyerAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def get(self,request,*args,**kwargs):
        google_id = request.GET['google_id']
        return Response(data=get_buyer(google_id=google_id))

    def put(self,request,*args,**kwargs):
        data = request.data
        if "google_id" not in data:
            raise ValueError("No google id!")
        if "name" not in data:
            raise ValueError("No name!")
        if "ntu_email" not in data:
            raise ValueError("No ntu email!")
        if "contact_number" not in data:
            raise ValueError("No contact number!")
        if "gender" not in data:
            raise ValueError("No gender in request!")
        if "birth_date" not in data:
            raise ValueError("No birth date!")
        if "course" not in data:
            raise ValueError("No course!")
        if "graduation_year" not in data:
            raise ValueError("No graduation year!")
        if "address" not in data:
            raise ValueError("No address!")
        if "origin_city" not in data:
            raise ValueError("No origin city!")
        if "company" not in data:
            raise ValueError("No company!")
        user = user_get(google_id=data['google_id'])
        new_data = update_buyer(user,data)
        return Response(data=new_data)

    def post(self,request,*args,**kwargs):
        data = request.data
        if "google_id" not in data:
            raise ValueError("No google id!")
        if "name" not in data:
            raise ValueError("No name!")
        if "ntu_email" not in data:
            raise ValueError("No ntu email!")
        if "contact_number" not in data:
            raise ValueError("No contact number!")
        if "gender" not in data:
            raise ValueError("No gender in request!")
        if "birth_date" not in data:
            raise ValueError("No birth date!")
        if "course" not in data:
            raise ValueError("No course!")
        if "graduation_year" not in data:
            raise ValueError("No graduation year!")
        if "address" not in data:
            raise ValueError("No address!")
        if "origin_city" not in data:
            raise ValueError("No origin city!")
        if "company" not in data:
            raise ValueError("No company!")
        user = user_get(google_id=data['google_id'])
        new_data,status = create_buyer(user,data)
        if not status:
            raise ValueError("Buyer not created!")
        return Response(data=new_data)

class SellerAPI(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self,request,*args,**kwargs):
        pass

class OTPAPI(APIView):
    authentication_classes=()
    permission_classes=()
    def post(self,request,*args,**kwargs):
        data = request.data
        if(verifyOTP(data['otp'],data['email'])):
            return Response({"verified":True})
        return Response({"verified":False})

    def get(self,request,*args,**kwargs):
        data = request.GET['email']
        otp=encodeOTP(data).at(0)
        sent=sendEmail(otp,data)
        return Response({"sent":sent})
