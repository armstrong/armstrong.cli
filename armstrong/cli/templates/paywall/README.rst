Paywall Demo
============

This template shows a working version of paywall code. The paywall is declared
in ``urls/defaults.py``. By default, the ``SubscriptionPaywall`` returns a 304 when
access is denied, but it has been overriden to render the
``permission_denied.html`` template instead. The only view that needs to be
protected is the ``ArticleDetailView``.

The third article on the front page, 'Help Wanted' is protected. When not
logged in, the ``permission_denied.html`` will be rendered, but when logged in as a
staff member or as the user with the username 'user' and password of 'user' you
will see the normal ``article.html`` template.
