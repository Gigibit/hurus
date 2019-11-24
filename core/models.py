import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _

from tinymce.models import HTMLField

GERMAN = 'DE'
ENGLISH = 'EN'
ITALIAN =  'IT'
LANGUAGES = (
    (GERMAN, 'German'),
    (ITALIAN, 'Italian'),
    (ENGLISH, 'English'),
)


FREETIME     = 'FT'
MARKET_PLACE = 'MP'


TYPES = (
    (FREETIME, 'Freetime'),
    (MARKET_PLACE, 'MarketPlace'),
)



def activity_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/img/activities/team_{0}/{1}'.format(instance.team.id if instance.team else 0, filename)

def course_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'static/img/course/{0}/{1}'.format(instance.id, filename)



class Agency(models.Model):
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    p_iva = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EncouragingSentence(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default=GERMAN,
    )



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to=course_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(
            max_length=2,
            choices=LANGUAGES,
            default=GERMAN,
    )
    def __str__(self):
        return self.title

class CourseSection(models.Model):
    title   = models.CharField(max_length=200)
    content = HTMLField()
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.title = self.course.title + ' - Section ' + str(len(self.course.sections.all()) + 1) 
        super(CourseSection, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

#        elif user.title == EMPLOYEE:
#            Employee(profile=user).save()
#
        return user

    def create_user(self, email, password=None, **extra_fields):
        print('create_user')
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    preferred_language = models.CharField(
            max_length=2,
            choices=LANGUAGES,
            default=GERMAN,
    )
    read_encouraging_sentences = models.ManyToManyField(EncouragingSentence)
    agency = models.ForeignKey(Agency, null=True, on_delete=models.DO_NOTHING)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager() ## This is the new line in the User model. ##
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen_courses            = models.ManyToManyField(Course, null=True, related_name='seen_by')
    course_to_see           = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    last_seen_course_date   = models.DateTimeField(null=True)
    
    def has_to_get_new_course(self):
        return not self.course_to_see or (datetime.today().date() - self.last_seen_course_date.date()).days < 1



# Create your models here.
class Manager(UserProfile):
    
    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'

    def __str__(self):
        return self.email

class Team(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ManyToManyField(Manager, null=True)



class Activity(models.Model):
    activity_type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=FREETIME,
    )
    i18n_key = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    icon = models.FileField(upload_to=activity_directory_path)
    team = models.ForeignKey(Team, null=True, related_name='activities', on_delete=models.CASCADE)    



class Employee(UserProfile):
    team                 = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name='employees')
    last_seen_survey     = models.DateTimeField(null=True)
    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def has_seen_daily_survey(self):
        return self.last_seen_survey and (datetime.today().date() - self.last_seen_survey.date()).days < 1



class ToughtOption(models.Model):
    i18n_key = models.CharField(max_length=50, null=True)
    text = models.CharField(max_length=50, null=True)
    is_happy = models.BooleanField(default=False) # :(

class Mood(models.Model):
    value = models.IntegerField()
    i18n_key = models.CharField(max_length=50, null=True)
    icon = models.FileField()



class Tought(models.Model):


    tought_type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=FREETIME,
    )

    mood = models.ForeignKey(Mood, on_delete=models.DO_NOTHING)
    tought_options = models.ManyToManyField(ToughtOption, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.DO_NOTHING, related_name='toughts')
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    motivational_quote = models.ForeignKey(EncouragingSentence, null=True, on_delete=models.DO_NOTHING)


    def to_public_dict(self):
        tought_options = []

        for option in self.tought_options.all(): 
            tought_options.append({
                'i18n_key' : option.i18n_key,
                'text' : option.text,
                'is_happy' : option.is_happy
            })
        activities = []
        for activity in self.activities.all(): 
            activities.append({
                'i18n_key' : activity.i18n_key,
                'name' : activity.name,
                'icon' : activity.icon.name
            })

        tought =  {
            'tought_type' : self.tought_type,
            'mood' : {
                'i18n_key':self.mood.i18n_key,
                'icon' : self.mood.icon.name,
                'value' : self.mood.value
            },
            'activities': json.dumps(activities),
            'employee' : self.employee.email,
            'tought' : self.text,
            'tought_options': json.dumps(tought_options),
            'created_at' : self.created_at
        }
        if self.motivational_quote:
            tought['motivational_quote'] = model_to_dict(self.motivational_quote)
        return tought