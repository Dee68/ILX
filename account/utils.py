from django.core.mail import EmailMessage
from django.conf import settings


class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER, to=[data['user']])
        email.send()
