import logging

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.utils.importlib import import_module

from .utils import translate

logger = logging.getLogger(__name__)


class EmailBackend(BaseEmailBackend):

    def __init__(self, backend=None, *args, **kwargs):
        if backend is None:
            backend = getattr(settings, 'DEMAIL_BACKEND',
                              'django.core.mail.backends.console.EmailBackend')
        logger.debug('EMAIL_BACKEND = %r', backend)

        if isinstance(backend, basestring):
            module, cls = backend.rsplit('.', 1)
            backend = getattr(import_module(module), cls)

        self.backend = backend()

    def send_messages(self, email_messages):
        return self.backend.send_messages(map(translate, email_messages))
