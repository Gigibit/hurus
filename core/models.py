from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import AbstractUser, BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import ugettext_lazy as _

GERMAN = 'DE'
ENGLISH = 'EN'
ITALIAN =  'IT'
LANGUAGES = (
    (GERMAN, 'German'),
    (ITALIAN, 'Italian'),
    (ENGLISH, 'English'),
)


class Agency(models.Model):
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    p_iva = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EncouragingSentence(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default=GERMAN,
    )

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





class Employee(UserProfile):
    
    team                = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, related_name='employees')
    last_seen_survey    = models.DateField(null=True)


    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def has_seen_daily_survey(self):
        today = datetime.today()
        return self.last_seen_survey and (today - self.last_seen_survey).days >= 1


class Tought(models.Model):
    HAPPY = 'HP'
    SAD = 'SD'
    ANGRY = 'NG'
    IN_GOOD_MOOD = 'GM'
    AWFUL = 'AW'
    INSPIRED = 'SP'
    MOODS = (
        (HAPPY, 'Happy'),
        (SAD, 'Sad'),
        (ANGRY, 'Angry'),
        (IN_GOOD_MOOD, 'In good mood'),
        (AWFUL, 'Awful'),
        (INSPIRED, 'Inspired'),
    )
 


    mood = models.CharField(
                max_length=2,
                choices=MOODS,
                default=SAD,
            )
    employee = models.ForeignKey(Employee, null=True, on_delete=models.DO_NOTHING, related_name='toughts')
    text = models.CharField(max_length=100)
    when = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

