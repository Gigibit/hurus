from django.db import models


# Create your models here.
class Manager(models.Model):
    email = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)


class Agency(models.Model):
    name = models.CharField(max_length=50)
    p_iva = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)




class Employee(models.Model):
    email = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL, related_name='employees')
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)



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



