from __future__ import absolute_import, unicode_literals

# import threading
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError

from celery import shared_task
from Imagify.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError

from django.core import mail

from smtplib import SMTP
import smtplib,ssl
import os
from .models import User
from django.contrib.auth.forms import PasswordResetForm


# from .views import gogo
# connection = mail.get_connection()




# class EmailThread(threading.Thread):
#     def __init__(self,email):
#         self.email=email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()

@shared_task(bind=True)
def send_verification_emailid(self,email_subject,email_body,from_email,empass,to):
        # for i in range(5):
        #         print(i)
        # print("Done")
        # print(email_subject)
        # print(email_body)
        # print(to)
        # print(settings.EMAIL_HOST_USER,type(settings.EMAIL_HOST_USER))
        # print(EMAIL_HOST_USER,type(EMAIL_HOST_USER))
        # print(os.environ.get('EMAIL_HOST_USER'),type(os.environ.get('EMAIL_HOST_USER')))
        # print(str(os.environ.get('EMAIL_HOST_USER')),type(str(os.environ.get('EMAIL_HOST_USER'))))


        # send_mail_to(email_subject,email_body,to)
        # print(connection)

        # connection.open()'
        message = f"""From: {from_email}\nTo: {to}\nSubject: {email_subject}\n\n{email_body}
        """
        server = smtplib.SMTP(settings.EMAIL_HOST, 587)
        # server = smtplib.SMTP_SSL(settings.EMAIL_HOST, 465)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.login(from_email, empass)
        server.sendmail(from_email,to, message)
        server.quit()

        # SMTP.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        # email=EmailMessage(subject=email_subject,body=email_body,
        #         from_email=from_email,
        #         to=[to],
        #         )
        # email.send()
        # connection.send_messages([email])
        # connection.close()

        # try:
        #         send_mail(email_subject,
        #         email_body,
        #         # from_email=settings.DEFAULT_FROM_EMAIL,
        #         settings.EMAIL_HOST_USER,
        #         [to],
        #         fail_silently=False
        #         )
        # except BadHeaderError:
        #         print("Nooooo Bad")
        # send_mail("Hello","Ok",settings.EMAIL_HOST_USER,[to])


@shared_task
def send_mail(subject_template_name, email_template_name, context,
              from_email, to_email, html_email_template_name):
    context['user'] = User.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )

    