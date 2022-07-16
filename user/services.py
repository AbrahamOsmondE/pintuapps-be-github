from django.core.exceptions import ValidationError
from django.http import HttpResponse
import requests
from .models import User, Buyer, Seller
from rest_framework_jwt.settings import api_settings
import datetime
import pyotp
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

GOOGLE_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

INTERVAL_OTP = 10

def google_validation(access_token):
    response = requests.get(
        GOOGLE_TOKEN_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError("Access token invalid!")
    
    return True

def jwt_login(response: HttpResponse,user:User):
    jwt_payload = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload(user)
    token = jwt_encode(payload)

    params = {
        'expires': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'domain': "http://127.0.0.1:8000",
        'path': "/",
        'secure': True,
        'httponly': True,
        'samesite': None
    }

    response.set_cookie(key=api_settings.JWT_AUTH_COOKIE, value=token, **params)

    return response, token

def jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    return {
        'token':token,
        'user':user_get_me(user=user, registered=True),
        'issued_at':datetime.datetime.fromtimestamp(issued_at).strftime("%A, %B %d, %Y %I:%M:%S")
    }

def create_user(email,google_id):
    return User.objects.create_user(email=email,google_id=google_id, password=None)

def user_delete(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValueError("No user found upon deletion!")
    user.delete()

def user_get(user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        return user
    raise ValueError("user not found!")

def user_get_create(email,google_id):
    user = User.objects.filter(google_id=google_id).first()
    if user:
        return user, True
    return create_user(email=email, google_id=google_id), False

def user_get_me(user, registered):
    return {
        "user_id":user.id,
        "email":user.email,
        "user_type":user.user_type,
        "registered":registered
    }

def user_get_all():
    buyers = Buyer.objects.all()
    data=[]
    for i in range(len(buyers)):
        data.append({"name":buyers[i].name, "user_id":buyers[i].user.id})
    return data

def create_buyer(user,data):
    user.user_type="buyer"
    user.save()
    buyer = Buyer(user=user,name=data['name'],ntu_email=data['ntu_email'], contact_number=data['contact_number'], gender=data['gender'], birth_date=data['birth_date'], course=data['course'], graduation_year=data['graduation_year'], address=data['address'], origin_city=data['origin_city'], company=data['company'], emergency_name=data['emergency_name'], emergency_contact=data['emergency_contact'])
    buyer.save()
    find = Buyer.objects.get(user=user)
    if not find:
        return None, False
    data = {
        "user_id": buyer.user.id,
        "user_type": user.user_type,
        "name": buyer.name,
        "personal_email": user.email,
        "ntu_email": buyer.ntu_email,
        "contact_number": buyer.contact_number,
        "gender": buyer.gender,
        "birth_date": buyer.birth_date,
        "course": buyer.course,
        "graduation_year": buyer.graduation_year,
        "address": buyer.address,
        "origin_city": buyer.origin_city,
        "company": buyer.company,
        "emergency_name": buyer.emergency_name,
        "emergency_contact": buyer.emergency_contact
    }
    return data, True

def update_buyer(user,data):
    buyer = Buyer.objects.get(user=user)
    buyer.name = data['name']
    buyer.ntu_email = data['ntu_email']
    buyer.contact_number = data['contact_number']
    buyer.gender = data['gender']
    buyer.birth_date = data['birth_date']
    buyer.course = data['course']
    buyer.graduation_year = data['graduation_year']
    buyer.address = data['address']
    buyer.origin_city = data['origin_city']
    buyer.company = data['company']
    buyer.emergency_contact = data['emergency_contact']
    buyer.emergency_name = data['emergency_name']
    buyer.save()
    data = {
        "user_id": buyer.user.id,
        "user_type": buyer.user.user_type,
        "name": buyer.name,
        "personal_email":buyer.user.email,
        "ntu_email": buyer.ntu_email,
        "contact_number": buyer.contact_number,
        "gender": buyer.gender,
        "birth_date": buyer.birth_date,
        "course": buyer.course,
        "graduation_year": buyer.graduation_year,
        "address": buyer.address,
        "origin_city": buyer.origin_city,
        "company": buyer.company,
        "emergency_contact": buyer.emergency_contact,
        "emergency_name": buyer.emergency_name
    }
    return data

def get_buyer(user_id):
    user = user_get(user_id=user_id)
    buyer = Buyer.objects.filter(user=user).first()
    if not buyer:
        raise ValueError("Buyer not found!")
    data = {
        "user_id": buyer.user.id,
        "name": buyer.name,
        "personal_email":buyer.user.email,
        "ntu_email": buyer.ntu_email,
        "contact_number": buyer.contact_number,
        "gender": buyer.gender,
        "birth_date": buyer.birth_date,
        "course": buyer.course,
        "graduation_year": buyer.graduation_year,
        "address": buyer.address,
        "origin_city": buyer.origin_city,
        "company": buyer.company,
        "emergency_contact": buyer.emergency_contact,
        "emergency_name": buyer.emergency_name
    }
    return data

def get_seller(user_id):
    user = user_get(user_id=user_id)
    seller = Seller.objects.filter(user=user).first()
    if not seller:
        raise ValueError("Seller not found!")
    data={
        "user_id":seller.user.id,
        "name":seller.name,
        "user_type":seller.user.user_type,
        "personal_email":seller.user.email,
        "contact_number":seller.contact_number,
        "gender":seller.gender
    }
    return data

def create_seller(user,data):
    pass

def encodeOTP(user):
    secret_otp = pyotp.random_base32()
    user.secret_otp = secret_otp
    user.save()
    totp = pyotp.TOTP(user.secret_otp, interval=INTERVAL_OTP)
    otp = totp.now()
    return otp

def verifyOTP(user, otp):
    totp = pyotp.TOTP(user.secret_otp, interval=INTERVAL_OTP)
    return totp.verify(otp)

def sendEmail(otp,email):
    check = email.split("@")
    if(check[1]!='ntu.edu.sg' and check[1]!='e.ntu.edu.sg'):
        raise ValueError("Not an NTU Email account!")
    mail_subject = "PINTU App OTP Verification Code"
    message = render_to_string('templates.html', {
        "otp":otp
    })
    to_email = email
    send_email = EmailMessage(mail_subject,message, to=[to_email])
    send_email.send()
    return True