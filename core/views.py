from django.shortcuts import render, redirect
from django.http import JsonResponse
import os, base64, json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from core.models import *
from helloCurus.settings import BASE_DIR
from django.forms.models import model_to_dict


def get_icons():
    path = os.path.join(BASE_DIR, 'static/img/freetime_available_icons')
    img_list =os.listdir(path)   
    return ['img/freetime_available_icons/' + src for src in img_list]



def get_toughts():
    return ToughtOption.objects.all()


def get_freetime_available_choose():
    return Activity.objects.filter(team=None)


MY_SECRET_FOR_EVER = 'Sara Cannella' # This is input in the form of a string
KDF = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'salt_',
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(KDF.derive(MY_SECRET_FOR_EVER.encode())) # Can only use kdf oncefrom cryptography.fernet import Fernet



def statistics_manager(request):
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




def home_employee(request, employee):
    return render(request, 'core/employee/index.html', {
    'foo': 'bar',
    })


def statistics_employee(request, employee):
    toughts = [ tought.to_public_dict() for tought in Tought.objects.all() ]
    moods = Mood.objects.all()
    return render(request, 'core/employee/statistics.html', {
        'moods' : moods,
        'toughts' : toughts,
    })


def happy_curus_employee(request, employee):
    return render(request, 'core/employee/happy_curus.html', {
        'foo': 'bar',
    })


def e_learning_employee(request, employee):
    return render(request, 'core/employee/e_learning.html', {
        'foo': 'bar',
    })


@csrf_exempt
def add_activity(request):
    if request.method == 'POST':
        employee = Employee.objects.get(email = request.user.email)
        activity_name   = request.POST['name']
        image_src       = request.POST['src']
        print(str(employee.team))

        activity = Activity.objects.create(
            team = employee.team,
            name  = activity_name,
            icon =  image_src
        )
        activity.save()
        return JsonResponse({
            'icon' : activity.icon.name,
            'name' : activity.name,
            'id'   : activity.pk
        })

    
def check_survey(fn, request, employee):
    toughts = get_toughts()
    default_freetime_choose = get_freetime_available_choose()
    available_icons = get_icons()
    moods = Mood.objects.all()

    if employee.team:
        team_freetime_choose = Activity.objects.filter(team=employee.team)
    else:
        team_freetime_choose = []
        employee = Employee.objects.get(email = request.user.email)
    if not employee.has_seen_daily_survey():
        return render(request, 'core/employee/evaluate_mood.html', {
            'toughts':toughts,
            'moods' : moods,
            'available_icons' : available_icons,
            'freetime_available_choose': default_freetime_choose,
            'team_freetime_available_choose': team_freetime_choose
        })
    return fn(request, employee)

def get_employee_from_request_user(user):
    try:
        return Employee.objects.get(email = user.email)
    except Employee.DoesNotExist:
        return False


@csrf_exempt
def tought_for_day(request):

    try:
        toughts = Tought.objects.filter(
            created_at__day=request.GET['day'],
            created_at__month=request.GET['month'],
            created_at__year=request.GET['year'] 
        )
        return JsonResponse({
            'toughts' : [t.to_public_dict() for t in toughts]
        })
    except Tought.DoesNotExist:
        return JsonResponse({})

@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        employee = Employee.objects.get(email = request.user.email)
        employee.last_seen_survey = datetime.now()
        employee.save()
        mood = Mood.objects.get(pk=request.POST['selected_mood'])
        tought_options = list(ToughtOption.objects.filter(pk__in=request.POST.getlist('toughts[]')))
        activities = Activity.objects.filter(pk__in=request.POST.getlist('activities[]'))
        tought = Tought.objects.create(  
                        mood=mood,
                        text=request.POST['current_tought'],
                        employee=employee
                        )
        if tought_options and len(tought_options) > 0:
            tought.tought_options.add(*tought_options)

        if activities and len(activities) > 0:
            tought.activities.add(*activities)


        return JsonResponse({
          'status' : 200,
          'stoc' : 'stoc'
        })
    return None


def home(request):
    employee = get_employee_from_request_user(request.user)
    return check_survey(home_employee, request, employee) if employee else home_manager(request)

def statistics(request):
    employee = get_employee_from_request_user(request.user)
    return check_survey(statistics_employee, request, employee) if employee else statistics_manager(request)

def happy_corus(request):
    employee = get_employee_from_request_user(request.user)
    return check_survey(happy_curus_employee, request, employee) if employee else  happy_curus_manager(request)

def e_learning(request):
    employee = get_employee_from_request_user(request.user)
    return check_survey(e_learning_employee, request, employee) if employee else e_learning_manager(request)



def home_manager(request):
    return render(request, 'core/manager/index.html', {
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












# def upload_file(request, user_dir, _filename = None):
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             print('hey niente', file=sys.stdout)
#             return False
#         file = request.files['file']
#         #TODO: convert image to png always

#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             print('hey niente', file=sys.stdout)
#             return False

#         if file and allowed_file(file.filename):
#             filename =  _filename if _filename else secure_filename(file.filename)
#             path = os.path.join(app.config['UPLOAD_FOLDER'], user_dir, filename)
#             os.makedirs(os.path.dirname(path), exist_ok=True)
#             file.save(path)
#             return url_for('static', filename=os.path.join('images',user_dir, filename), _external=True)
#     else:
#         print('method not was allowed')
#         return False
