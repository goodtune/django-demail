# demail

This is a reusable email backend that will rewrite the recipient lists on any
messages to ensure they are not leaked to users in pre-production environments.

## Uses

You have a project that requires a pre-production environment for production
support. You have production data, including real email addresses, for users
and you'd like to ensure that any notifications sent by your application will
never escape to be delivered to the user.

However to validate your testing of an issue you still need to see the email
delivered, routed by exactly the same mechanisms as in production.

By using ``demail`` as your backend you can configure your pre-production
environment as for production, and let it take care of re-addressing emails for
you - no data masking required.