# -*- coding: utf-8 -*-
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


def send_email(subject, html_content, mails_to_send):
    from_email, to = 'WUAPPA' + '<' + DEFAULT_FROM_EMAIL + '>', mails_to_send
    text_content = strip_tags(html_content.replace('<br>', '\r\n').replace('</p>', '\r\n\r\n'))
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)  # Do not raise exception
