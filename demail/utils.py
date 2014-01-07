import re

from . import logger

DEMAIL_ALLOWED_RECIPIENTS = ()
DEMAIL_ALLOWED_DOMAINS = ()

DEMAIL_REWRITE_MAILBOX = None
DEMAIL_REWRITE_DOMAIN = 'example.com'

TRANS = {
    r'@': '=',
    r'\+': '-',
}


def translate(message):
    """
    Map the ``rewrite_recipient_address`` function to each addressee of this
    message.
    """
    message.to = map(rewrite_recipient_address, message.to)
    message.cc = map(rewrite_recipient_address, message.cc)
    message.bcc = map(rewrite_recipient_address, message.bcc)
    return message


def rewrite_recipient_address(addr):
    """
    Given a destination email address, determine if it is acceptable to
    deliver email directly to this address. If it is not then we rewrite the
    value so that delivery will go to an alternative mailbox.

    The value of ``email`` is assumed to be correct - the Django reference
    implementation ``django.core.mail.backends.smtp.EmailBackend`` does not
    perform any validation, so nor shall we.
    """
    # if addr is specifically declared deliverable, let it straight through
    if addr in DEMAIL_ALLOWED_RECIPIENTS:
        logger.debug('%s in DEMAIL_ALLOWED_RECIPIENTS - no rewrite.', addr)
        return addr

    # if the domain part of the addr is declared a deliverable mail exchange,
    # also let it through.
    localpart, domain = addr.split(u'@', 1)
    if domain in DEMAIL_ALLOWED_DOMAINS:
        logger.debug('%s in DEMAIL_ALLOWED_DOMAINS - no rewrite for %s.',
                     domain, addr)
        return addr

    # FIXME: this needs to be more robust, but for now we shall simply replace
    # any `@` or `+` symbols from the ``addr`` and making this the localpart
    # of an address at the destination mail exchange.
    localpart = addr
    for pat, repl in TRANS.items():
        localpart = re.sub(pat, repl, localpart)

    output = '@'.join([localpart, DEMAIL_REWRITE_DOMAIN])
    logger.warning('%s -> %s', addr, output)
    return output
