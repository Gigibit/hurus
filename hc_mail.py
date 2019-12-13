#! /usr/bin/env python3
import sys, os, django
django.setup()

from django.core.mail import EmailMessage
from core.models import Employee, Manager


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helloCurus.settings")


from django.core.mail import send_mail

def get_email_body_for_employee(employee):
    return 'brah!'
def get_email_body_for_manager(manager):
    return 'brah!'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    message = 'Your newsletter.'

    for e in Employee.objects.all():
        if e.agency.enabled:
            newsletters = get_email_body_for_employee(e)
            EmailMessage("HappyCurus daily login!", newsletters, to=[e.email]).send()

    
    for m in Manager.objects.filter():
        if m.agency.enabled:
            newsletters = get_email_body_for_manager(m)
            EmailMessage("HappyCurus daily login!", newsletters, to=[m.email]).send()


if __name__ == '__main__':
    main()