from django.shortcuts import render, redirect
from django.http import JsonResponse
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import login

from core.models import *

def get_toughts():
    return [
    {
      'i18n_key': "ACTIVE",
      'is_happy': True
    },

    {
      'i18n_key': "FOCUSED",
      'is_happy': True
    },
    {
      'i18n_key': "JOYFUL",
      'is_happy': True
    },
    {
      'i18n_key': "INTERESTED",
      'is_happy': True
    },
    {
      'i18n_key': "SERENE",
      'is_happy': True
    },
    {
      'i18n_key': "HOPEFUL",
      'is_happy': True
    },
    {
      'i18n_key': "GLAD",
      'is_happy': True
    },
    {
      'i18n_key': "SURPRISED",
      'is_happy': True
    },
    {
      'i18n_key': "CHEERFUL",
      'is_happy': True
    },
    {
      'i18n_key': "CONFIDENT",
      'is_happy': True
    },
    {
      'i18n_key': "RELIEVED",
      'is_happy': True
    },
    {
      'i18n_key': "IN_LOVE",
      'is_happy': True
    },
    {
      'i18n_key': "ENTHUSIASTIC",
      'is_happy': True
    },
    {
      'i18n_key': "RELAXED",
      'is_happy': True
    },
    {
      'i18n_key': "SATISFACTED",
      'is_happy': True
    },
    {
      'i18n_key': "PROUD",
      'is_happy': True
    },
    {
      'i18n_key': "SAD",
    },
    {
      'i18n_key': "ASHAMED",
    },
    {
      'i18n_key': "ANXIOUS",
    },
    {
      'i18n_key': "AFRAID",
    },
    {
      'i18n_key': "DEPRESSED",
    },
    {
      'i18n_key': "LONELY",
    },
    {
      'i18n_key': "DELUDED",
    },
    {
      'i18n_key': "ANNOYED",
    },
    {
      'i18n_key': "COLD",
    },
    {
      'i18n_key': "CONFUSED",
    },
    {
      'i18n_key': "PASSIVE",
    },
    {
      'i18n_key': "PREOCCUPIED",
    },
    {
      'i18n_key': "INSECURE",
    },
    {
      'i18n_key': "REPRESSED"
    },
    {
      'i18n_key':"FRURSTRATED"
    },
    {
      'i18n_key': "DISGUSTED",
    },
    {
      'i18n_key': "GUILTY",
    },
    {
      'i18n_key': "DISCOURAGED"
    }
  ]
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





    
def check_survey(fn, request):
    toughts = get_toughts()
    employee = Employee.objects.get(email = request.user.email)
    if not employee.has_seen_daily_survey():
        return render(request, 'core/employee/evaluate_mood.html', {
        'toughts':toughts,
        })
    return fn(request)

def is_manager(user):
    try:
        return Manager.objects.get(email = user.email)
    except Manager.DoesNotExist:
        return False

def home(request):
    print(str(request.user is Employee))
    return home_manager(request) if is_manager(request.user) else check_survey(home, request) 

def statistic(request):
    return statistic_manager(request) if is_manager(request.user) else check_survey(statistic_employee, request) 

def happy_corus(request):
    return happy_corus_manager(request) if is_manager(request.user) else check_survey(happy_corus_employee,request) 

def e_learning(request):
    return e_learning_manager(request) if is_manager(request.user) else check_survey(e_learning_employee,request) 



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
            'info_cripted':  encrypt(token)
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
