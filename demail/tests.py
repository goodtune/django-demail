"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(EMAIL_BACKEND='demail.backends.EmailBackend')
class DelegateEmailTest(TestCase):
    """
    It is necessary to override the ``EMAIL_BACKEND`` setting here, regardless
    of the value in the test_app, because the Django test runner will always
    force it to be ``'django.core.mail.backends.locmem.EmailBackend'`` when it
    sets up the testing environment.

    See http://stackoverflow.com/a/15053970 for details.
    """

    def setUp(self):
        self.recipient_list = [
            'gary@touch.asn.au',
            'john.reynolds@touchtechnology.com.au',
        ]

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_pass_through(self):
        mail.send_mail(u'Subject',
                       u'',
                       settings.DEFAULT_FROM_EMAIL,
                       self.recipient_list)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].to, self.recipient_list)

    @override_settings(DEMAIL_ALLOWED_DOMAINS=('touchtechnology.com.au',))
    def test_allowed_domains(self):
        mail.send_mail(u'Subject',
                       u'',
                       settings.DEFAULT_FROM_EMAIL,
                       self.recipient_list)

        recipients = [
            'gary=touch.asn.au@example.com',
            'john.reynolds@touchtechnology.com.au',
        ]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].to, recipients)

    @override_settings(DEMAIL_ALLOWED_RECIPIENTS=('gary@touch.asn.au',))
    def test_allowed_recipients(self):
        mail.send_mail(u'Subject',
                       u'',
                       settings.DEFAULT_FROM_EMAIL,
                       self.recipient_list)

        recipients = [
            'gary@touch.asn.au',
            'john.reynolds=touchtechnology.com.au@example.com',
        ]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].to, recipients)

    @override_settings(DEMAIL_REWRITE_DOMAIN='test.example.com')
    def test_rewrite_domain(self):
        mail.send_mail(u'Subject',
                       u'',
                       settings.DEFAULT_FROM_EMAIL,
                       self.recipient_list)

        recipients = [
            'gary=touch.asn.au@test.example.com',
            'john.reynolds=touchtechnology.com.au@test.example.com',
        ]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].to, recipients)

    @override_settings(DEMAIL_REWRITE_RECIPIENT='test@example.com')
    def test_rewrite_recipient(self):
        mail.send_mail(u'Subject',
                       u'',
                       settings.DEFAULT_FROM_EMAIL,
                       self.recipient_list)

        recipients = [
            'test+gary=touch.asn.au@example.com',
            'test+john.reynolds=touchtechnology.com.au@example.com',
        ]

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject')
        self.assertEqual(mail.outbox[0].to, recipients)

    # @override_settings(
    #     DEMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
    # def test_backend(self):
    #     mail.send_mail(u'Subject',
    #                    u'',
    #                    settings.DEFAULT_FROM_EMAIL,
    #                    self.recipient_list)
