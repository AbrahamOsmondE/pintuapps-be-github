from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.blacklist.models import BlacklistedToken
from rest_framework import serializers

from datetime import datetime

from .decorators import admin_api, all_api, buyer_api, seller_api

from .services import encodeOTP, get_seller, google_validation, sendEmail, user_get, user_get_all, user_get_me, jwt_login, user_delete, user_get_create, create_buyer, update_buyer, get_buyer, verifyOTP

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
            "user_id":user_data['user_id'],
            "user_type":user_data['user_type'],
            "registered":user_data['registered'],
            "token":token
        }
        response = Response(data=data_response)
        return response

    @admin_api
    def delete(self,request,*args,**kwargs):
        # data = request.GET['user_id']
        data = request.user.id
        user_delete(user_id=data)
        return Response(status=status.HTTP_200_OK)

class LogoutAPI(APIView):
    authentication_classes=()
    permission_classes=()
    def post(self,request,*args,**kwargs):
        data = request.data
        user_id = request.headers['user-id']
        if 'token' not in data:
            raise ValueError("No token!")
        token = data['token']
        blacklisted = BlacklistedToken(token=token, user_id=user_get(user_id).id, expires_at=datetime.now())
        blacklisted.save()
        return Response({'message':"Token has been blacklisted",'success':True})


class UsersAPI(APIView):
    def get(self,request,*args,**kwargs):
        response={"users":user_get_all()}
        return Response(data=response)

class BuyerAPI(APIView):
    @buyer_api
    def get(self,request,*args,**kwargs):
        # user_id = request.GET['user_id']
        user_id = request.user.id
        return Response(data=get_buyer(user_id=user_id))

    @buyer_api
    def put(self,request,*args,**kwargs):
        # user_id = request.headers['user-id']
        user_id = request.user.id
        data = request.data
        if not user_id:
            raise ValueError("No user_id!")
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
        if "emergency_contact" not in data:
            raise ValueError("No emergency contact!")
        if "emergency_name" not in data:
            raise ValueError("No emergency name")
        user = user_get(user_id=user_id)
        new_data = update_buyer(user,data)
        return Response(data=new_data)

    @all_api
    def post(self,request,*args,**kwargs):
        # user_id = request.headers['user-id']
        user_id = request.user.id
        data = request.data
        if not user_id:
            raise ValueError("No user_id!")
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
        if "emergency_contact" not in data:
            raise ValueError("No emergency contact!")
        if "emergency_name" not in data:
            raise ValueError("No emergency name")
        user = user_get(user_id=user_id)
        new_data,status = create_buyer(user,data)
        if not status:
            raise ValueError("Buyer not created!")
        return Response(data=new_data)

class SellerAPI(APIView):
    @seller_api
    def get(self,request,*args,**kwargs):
        # user_id = request.GET['user_id']
        user_id = request.user.id
        return Response(data=get_seller(user_id=user_id))

class OTPAPI(APIView):
    @all_api
    def post(self,request,*args,**kwargs):
        user = request.user
        otp = request.data['otp']
        if not otp:
            raise ValueError("No otp!")
        if(verifyOTP(user, otp)):
            return Response({"verified":True})
        return Response({"verified":False})
    @all_api
    def get(self,request,*args,**kwargs):
        data = request.GET['email']
        otp = encodeOTP(request.user)
        sent = sendEmail(otp,data)
        return Response({"sent":sent})