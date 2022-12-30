from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings


def send_mail(to, template, context):
    html_content = render_to_string(
        f'accounts/emails/{template}.html', context)
    text_content = render_to_string(f'accounts/emails/{template}.txt', context)

    msg = EmailMultiAlternatives(
        context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_activation_email(request, email, code, uid):
    context = {
        'subject': ('Profile activation'),
        'uri': request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'code': code})),
    }

    send_mail(email, 'activate_account', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': 'Restore password',
        'uri': request.build_absolute_uri(
            reverse('restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'password_reset_email', context)
