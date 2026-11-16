===========
wagtail-2fa
===========

.. image:: https://img.shields.io/pypi/v/wagtail-2fa.svg
    :target: https://pypi.org/project/wagtail-2fa/

.. image:: https://github.com/labd/wagtail-2fa/actions/workflows/python-test.yml/badge.svg
    :target: https://github.com/labd/wagtail-2fa/actions/workflows/python-test.yml

.. image:: https://readthedocs.org/projects/wagtail-2fa/badge/?version=stable
    :target: https://wagtail-2fa.readthedocs.io/en/stable/?badge=stable

This Django app adds two factor authentication to Wagtail. Behind the scenes
it use django-otp_ which supports Time-based One-Time Passwords (TOTP). This
allows you to use various apps like Authy, Google Authenticator, or
1Password.


.. _django-otp: https://django-otp-official.readthedocs.io


Installation
============

.. code-block:: shell

   pip install wagtail-2fa


Then add the following lines to the ``INSTALLED_APPS`` list in your Django
settings:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'wagtail_2fa',
        'django_otp',
        'django_otp.plugins.otp_totp',
        # ...
    ]

Next add the required middleware to the ``MIDDLEWARE``. It should come
after the AuthenticationMiddleware:

.. code-block:: python

    MIDDLEWARE = [
        # .. other middleware
        # 'django.contrib.auth.middleware.AuthenticationMiddleware',

        'wagtail_2fa.middleware.VerifyUserMiddleware',

        # 'wagtail.core.middleware.SiteMiddleware',
        # .. other middleware
    ]

Migrate your database:

.. code-block:: shell

   python manage.py migrate



Settings
========

The following settings are available (Set via your Django settings):

- ``WAGTAIL_2FA_REQUIRED`` (default ``False``): When set to True all
  staff, superuser and other users with access to the Wagtail Admin site
  are forced to login using two factor authentication.
- ``WAGTAIL_2FA_OTP_TOTP_NAME`` (default: ``False``): The issuer name to
  identify which site is which in your authenticator app. If not set and
  ``WAGTAIL_SITE_NAME`` is defined it uses this. sets ``OTP_TOTP_ISSUER``
  under the hood.


Making 2FA optional
===================

With the default ``VerifyUserMiddleware`` middleware, 2FA is enabled for every user.
To make 2FA optional, use the ``VerifyUserPermissionsMiddleware`` middleware instead.

To do so, use the ``VerifyUserPermissionsMiddleware`` middleware instead of the ``VerifyUserMiddleware`` in your Django settings:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        # 'wagtail_2fa.middleware.VerifyUserMiddleware',
        'wagtail_2fa.middleware.VerifyUserPermissionsMiddleware',
        # ...
    ]

When this middleware is used, a checkbox is added to the group permissions
and 2FA can be enabled or disabled per group.

2FA is always enabled for superusers, regardless of the middleware used.


Sandbox
=======

First create a new virtualenv with Python 3.11 or newer and activate it. Then run
the following commands:

.. code-block:: shell

   make sandbox


You can then visit http://localhost:8000/admin/ and login with the following
credentials:

- E-mail: ``superuser@example.com``
- Password: ``testing``

Releasing
=========

Releases are managed with `changie <https://changie.dev>`_:

1. Add a changelog entry to your pull request with ``changie new``.
2. After merging to ``master``, a release pull request is opened (or updated)
   automatically, with the new version and the updated ``CHANGELOG.md``.
3. Merging the release pull request creates the GitHub release, which publishes
   the package to PyPI.
