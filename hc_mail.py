#! /usr/bin/env python3
import sys, os, django, json, datetime, base64
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helloCurus.settings")
django.setup()

from django.core.mail import send_mail 

from django.core.mail.message import EmailMultiAlternatives
from core.models import Employee, Manager
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

MY_SECRET_FOR_EVER = 'Sara Cannella' # This is input in the form of a string
KDF = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'salt_',
    iterations=100000,
    backend=default_backend()
)
base_url = 'https://happycurus.de' #'https://www.happycurus.de'

key = base64.urlsafe_b64encode(KDF.derive(MY_SECRET_FOR_EVER.encode())) # Can only use kdf oncefrom cryptography.fernet import Fernet

DE_DAYS = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
EN_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
IT_DAYS = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if datetime.datetime.today().weekday() >= 5:
        return


    for e in Employee.objects.all():
        if e.agency.enabled and e.email:
            token = get_token(e.email)
            newsletters = get_email_body_for_employee(e, token)
            mail = EmailMultiAlternatives("HappyCurus daily login!", 'Login in the application with %s' % (base_url + '/ax/' + token), 'hello@happycurus.de' ,to=[e.email])
            mail.attach_alternative(newsletters, 'text/html')
            mail.send(fail_silently=True)
            

    
    for m in Manager.objects.all():
        if m.agency.enabled and m.email:
            token = get_token(m.email)
            newsletters = get_email_body_for_manager(m, token)
            mail = EmailMultiAlternatives("HappyCurus daily login!", 'Login in the application with %s' % (base_url + '/ax/' + token), 'hello@happycurus.de' ,to=[m.email])
            mail.attach_alternative(newsletters, 'text/html')
            mail.send(fail_silently=True)









def get_email_body_for_employee(employee, token):
    username = employee.email
    language = employee.preferred_language

    if language.lower() == 'de':
        days = DE_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">DEIN PROFIL IST BEREIT</h1>' +\
            '                       <p class="message-body">' +\
            '                            Hallo ' + username + '!<br><br>' +\
            '                            Bist du bereit, an diesem %s<br>' +\
            '                            etwas zu bewirken?<br>' +\
            '                            Achte auf dich selber und dein Team,<br>' +\
            '                            indem du <a href="#">dein Profil</a> aktualisierest.<br><br>' +\
            '                            Klicke auf den <a href="'+ base_url +'/ax/' + token + '">link</a>, um darauf zuzugreifen.' +\
            '                        </p>'
    elif language.lower() == 'it':
        days = IT_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">Il TUO PROFILO È PRONTO</h1>' +\
            '                        <p class="message-body">' +\
            '                            CIAO ' + username + '!<br><br>' +\
            '                            Sei pronto ad avere un impatto positivo su<br>' +\
            '                            questo %s?<br>' +\
            '                            Prenditi cura di te stesso e del tuo <br>' +\
            '                            team aggiornando <a href="#">il tuo profilo</a>.<br><br>' +\
            '                            Clicca sul <a href="' + base_url + '/ax/' + token + '">link</a> per accedervi.' +\
            '                        </p>'
    else:
        days = EN_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">YOUR PROFILE IS READY</h1>' +\
            '                        <p class="message-body">' +\
            '                            Hi ' + username + '!<br><br>' +\
            '                            Are you ready to make a positive impact on<br>' +\
            '                            this %s?<br>' +\
            '                            Take care of yourself and your team by<br>' +\
            '                            updating <a href="#">your profile</a>.<br><br>' +\
            '                            Click on the <a href="' + base_url + '/ax/' + token + '">link</a> to access it.' +\
            '                        </p>'

    message_body = message_body % days[datetime.datetime.today().weekday()]
    return  '<html>' +\
            '    <body style="border: 3px solid #222;' +\
            '            padding: 21px;' +\
            '            position: relative;' +\
            '            height: 521px;">' +\
            '        <img width="120" src="' + base_url + '/static/img/website_assets/logo.png">' +\
            '        <div class="main">' +\
            '            <div class="message-container" style="' +\
            '            text-align: center;' +\
            '            background-color: #b3d5d6;' +\
            '            border-radius: 100%;' +\
            '            margin: 0 auto;' +\
            '            width: 300px;' +\
            '            height: 300px;' +\
            '            display: block;' +\
            '            padding: 60px;' +\
            '            position: absolute;' +\
            '            left: 0;' +\
            '            right: 0;' +\
            '            font-family: arial;">' +\
            '                <div class="message-wrapper">' +\
            '                    <div class="message-content">' +\
            '                       ' + message_body +\
            '                    </div>' +\
            '                </div>' +\
            '            </div>' +\
            '        </div>' +\
            '        <div class="claim-wrapper" style="text-align:right">'+\
            '           <img class="claim" width="184" height="75" src="' + base_url + '/static/img/website_assets/Happycurus-Claim_SW.png">'+\
            '       </div>' +\
            '    </body>' +\
            '</html>'


def get_email_body_for_manager(manager, token):
    username = manager.email
    language = manager.preferred_language

    if language.lower() == 'de':
        days = DE_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">DEIN TEAM LÄSST DICH<br>'+\
            '                       WISSEN, WIE SIE SICH FÜHLEN.</h1>' +\
            '                        <p class="message-body">' +\
            '                            Guten Tag ' + username + '!<br><br>' +\
            '                            Deine Mitarbeiter aktualisieren regelmäßig<br>' +\
            '                            ihre Profile. Willst du wissen, wie zufrieden<br>' +\
            '                            sie sind?<br><br>' +\
            '                            Klicke auf den <a href="' + base_url + '/ax/' + token + '">link</a>, um auf exklusive<br>' +\
            '                            statistiken deines Teams zuzugreifen.<br><br>' +\
            '                        </p>'

    elif language.lower() == 'it':
        days = IT_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">IL TUO TEAM TI STA<br>'+\
            '                       COMUNICANDO COME SI SENTE</h1>' +\
            '                        <p class="message-body">' +\
            '                            Ciao ' + username + '!<br><br>' +\
            '                            I tuoi dipendenti stanno aggiornando il<br>' +\
            '                            proprio profilo. Sei curioso di conoscere il<br>' +\
            '                            loro stato d’animo?<br><br>' +\
            '                            Clicca sul <a href="' + base_url + '/ax/' + token + '">link</a> per visualizzare le statistiche<br>' +\
            '                            a te riservate.<br><br>' +\
            '                        </p>'

    else:
        days = EN_DAYS
        message_body =  '<h1 class="message-title" style="' +\
            '            font-weight: bold;' +\
            '            font-size: 23px;' +\
            '            margin-top: 38px;">YOUR TEAM IS LETTING<br>YOU KNOW HOW THEY FEEL</h1>' +\
            '                        <p class="message-body">' +\
            '                            Hi ' + username + '!<br><br>' +\
            '                            Your employees are updating their<br>' +\
            '                            profiles. Do you want to know how<br>' +\
            '                            satisfied they are?<br><br>' +\
            '                            Click on the <a href="' + base_url + '/ax/' + token + '">link</a> to access exclusive<br>' +\
            '                            statistics about your team.<br><br>' +\
            '                        </p>'

#    message_body = message_body % days[datetime.datetime.today().weekday() - 1]
    return  '<html>' +\
            '    <body style="border: 3px solid #222;' +\
            '            padding: 21px;' +\
            '            position: relative;' +\
            '            height: 521px;">' +\
            '        <img width="120" src="' + base_url + '/static/img/website_assets/logo.png">' +\
            '        <div class="main">' +\
            '            <div class="message-container" style="' +\
            '            text-align: center;' +\
            '            background-color: #b3d5d6;' +\
            '            border-radius: 100%;' +\
            '            margin: 0 auto;' +\
            '            width: 300px;' +\
            '            height: 300px;' +\
            '            display: block;' +\
            '            padding: 60px;' +\
            '            position: absolute;' +\
            '            left: 0;' +\
            '            right: 0;' +\
            '            font-family: arial;">' +\
            '                <div class="message-wrapper">' +\
            '                    <div class="message-content">' +\
            '                         '+ message_body   +\
            '                    </div>' +\
            '                </div>' +\
            '            </div>' +\
            '        </div>' +\
            '        <div class="claim-wrapper" style="text-align:right">'+\
            '           <img class="claim" width="184" height="75" src="' + base_url + '/static/img/website_assets/Happycurus-Claim_SW.png">'+\
            '       </div>' +\
            '    </body>' +\
            '</html>' 



def get_token(for_email):
    expiring_time = datetime.date.today() + datetime.timedelta(days=1)
    return encrypt(str(json.dumps({
                'email':  for_email,
                'expiring_time' : expiring_time
            }, indent=4, sort_keys=True, default=str)
    ))

def encrypt(plain): 
    return Fernet(key).encrypt(plain.encode()).decode('utf-8')






if __name__ == '__main__': main()
