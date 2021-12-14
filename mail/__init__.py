from django.core.mail import send_mail


def send_fake_mail(*_):
    send_mail('Subject', 'This is a message', 'example@example.com', ['example@example.com'])
