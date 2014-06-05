import logging
import re

from django.conf import settings

logger = logging.getLogger(__name__)

DEMAIL_REWRITE_MAILBOX = None

TRANS = {
    r'@': '=',
    r'\+': '-',
}


def translate(message):
    """
    Map the ``rewrite_recipient_address`` function to each addressee of this
    message.
    """
    allowed_recipients = getattr(settings, 'DEMAIL_ALLOWED_RECIPIENTS', ())
    allowed_domains = getattr(settings, 'DEMAIL_ALLOWED_DOMAINS', ())
    rewrite_domain = getattr(settings, 'DEMAIL_REWRITE_DOMAIN', 'example.com')

    logger.debug('ALLOWED_RECIPIENTS = %r', allowed_recipients)
    logger.debug('ALLOWED_DOMAINS = %r', allowed_domains)
    logger.debug('REWRITE_DOMAIN = %r', rewrite_domain)

    rewrite = lambda addr: rewrite_recipient_address(addr,
                                                     allowed_domains,
                                                     allowed_recipients,
                                                     rewrite_domain)

    message.to = map(rewrite, message.to)
    message.cc = map(rewrite, message.cc)
    message.bcc = map(rewrite, message.bcc)

    return message


def rewrite_recipient_address(addr, allowed_domains, allowed_recipients,
                              rewrite_domain):
    """
    Given a destination email address, determine if it is acceptable to
    deliver email directly to this address. If it is not then we rewrite the
    value so that delivery will go to an alternative mailbox.

    The value of ``email`` is assumed to be correct - the Django reference
    implementation ``django.core.mail.backends.smtp.EmailBackend`` does not
    perform any validation, so nor shall we.
    """
    logger.debug('processing addr %r', addr)

    # if addr is specifically declared deliverable, let it straight through
    if addr in allowed_recipients:
        logger.debug('%r in ALLOWED_RECIPIENTS', addr)
        return addr

    # if the domain part of the addr is declared a deliverable mail exchange,
    # also let it through.
    localpart, domain = addr.split(u'@', 1)
    if domain in allowed_domains:
        logger.debug("%r matches ALLOWED_DOMAIN '%s'", addr, domain)
        return addr

    # FIXME: this needs to be more robust, but for now we shall simply replace
    # any `@` or `+` symbols from the ``addr`` and making this the localpart
    # of an address at the destination mail exchange.
    localpart = addr
    for pat, repl in TRANS.items():
        localpart = re.sub(pat, repl, localpart)

    output = '@'.join([localpart, rewrite_domain])
    logger.warning('rewriting %r -> %r', addr, output)
    return output
