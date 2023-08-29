import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from stackOverFlow.homeapplication.constants import redis_contants

logger = logging.getLogger(__name__)


class UserManager(models.Manager):
    def email_send(self, redis_conn, email, sms_code):
        pl = redis_conn.pipeline()  # redis管道技术
        pl.setex('send_%s' % email, redis_contants.USER_EMAIL_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % email, redis_contants.USER_SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        subject = "GDUT OSF系统 邮箱验证"
        html_message = '<p>尊敬的⽤户您好！</p>' \
                       '<p>感谢您使⽤GDUT综合测试系统。</p>' \
                       '<p>您的邮箱为：%s ，验证码为：%s</p>' % (email, sms_code)
        send_mail(subject, "", settings.EMAIL_FROM, [email], html_message=html_message)


