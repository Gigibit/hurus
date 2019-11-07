from django.shortcuts import render
from django.http import JsonResponse
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import login

from core.models import *


MY_SECRET_FOR_EVER = 'Sara Cannella' # This is input in the form of a string
password = MY_SECRET_FOR_EVER.encode() # Convert to type bytes
salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf oncefrom cryptography.fernet import Fernet







def home(request):
    return home_manager(request) if request.user.title == UserProfile.MANAGER else home_employee(request) 

def statistic(request):
    return statistic_manager(request) if request.user.title == UserProfile.MANAGER else statistic_employee(request) 

def happy_corus(request):
    return happy_corus_manager(request) if request.user.title == UserProfile.MANAGER else happy_corus_employee(request) 

def e_learning(request):
    return e_learning_manager(request) if request.user.title == UserProfile.MANAGER else e_learning_employee(request) 



def home_manager(request):
    return render(request, 'core/manager/index.html', {
        'foo': 'bar',
        })

def statistic_manager(request):
    return render(request, 'core/manager/satistics.html', {
    'foo': 'bar',
    })


def happy_curus_manager(request):
    return render(request, 'core/manager/happy_curus.html', {
    'foo': 'bar',
    })


def e_learning_manager(request):
    return render(request, 'core/manager/e_learning.html', {
    'foo': 'bar',
    })




def home_employee(request):
    return render(request, 'core/employee/index.html', {
    'foo': 'bar',
    })


def statistic_employee(request):
    return render(request, 'core/employee/statistics.html', {
    'foo': 'bar',
    })


def happy_curus_employee(request):
    return render(request, 'core/employee/happy_curus.html', {
    'foo': 'bar',
    })


def e_learning_employee(request):
    return render(request, 'core/employee/e_learning.html', {
    'foo': 'bar',
    })

























# Login engine
def engine(request):
    return JsonResponse({
     's':  encrypt('sara cannella')
    })


def login_user_from_token(request, token):
    try:
        decrypted_email = decrypt(token)
        user = UserProfile.objects.get(email = decrypted_email)
        login(request, user)
        return redirect('/')
    except (InvalidToken, UserProfile.DoesNotExist):
        return JsonResponse({
            'info_cripted':  encrypt('as@gmail.com'),
            's': str(can_access)
        })




def decrypt(plain): 
    return Fernet(key).decrypt(plain.encode()).decode('utf-8')

def encrypt(plain): 
    return Fernet(key).encrypt(plain.encode()).decode('utf-8')













import os

BS = 8
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def encode(phrase):
    key = MY_SECRET_FOR_EVER
    c1  = Blowfish.new(key.encode('utf8'), Blowfish.MODE_ECB)
    return c1.encrypt(pad(phrase))

def doDecrypt(phrase):
    c1  = Blowfish.new(key, Blowfish.MODE_ECB)
    return unpad(c1.decrypt(phrase))


def get_user(access_token):
    jwt = from_jwt(access_token)
    id = jwt.get('id', None)
    return jwt, decode(id) if id else None, jwt.get('email',None)


def allowed_file(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension[1:] in ALLOWED_EXTENSIONS

def upload_file(user_dir, _filename = None):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('hey niente', file=sys.stdout)
            return False
        file = request.files['file']
        #TODO: convert image to png always

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('hey niente', file=sys.stdout)
            return False

        if file and allowed_file(file.filename):
            filename =  _filename if _filename else secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], user_dir, filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file.save(path)
            return url_for('static', filename=os.path.join('images',user_dir, filename), _external=True)
    else:
        print('method not was allowed')
        return False
