django-le-twitter
=================

Twitter authentication that sucks.

Django-le-twitter provides almost nothing to let your users sign in with
twitter: two class-based views.

Django-le-twitter is based on Django >= 1.3 and `Tweepy`_.

.. _Tweepy: http://joshthecoder.github.com/tweepy/docs/index.html

The concept is simple: when a user successfully logs in using twitter (i.e.
you get a valid OAuth token), django-le-twitter executes a method that **you**
define. There is no model instance created, no login using contrib.auth, no
nothing. You decide.

Installation
------------

::

    pip install django-le-twitter

There's nothing to add to your INSTALLED_APPS. It just needs to be in your
python path. You need to add your Twitter app credentials to your Django
settings:

::

    CONSUMER_KEY = 'your key'
    CONSUMER_SECRET = 'your secret'

Usage
-----

Subclass the two views provided by django-le-twitter in one of your apps'
views. Actually, one of them doesn't strictly need to be subclassed.

::

    # app/views.py
    from django.http import HttpResponse

    from le_twitter import views

    authorize = views.Authorize.as_view()

    class Return(views.Return):

        def handle_error(self, error_msg, exception=None):
            return HttpResponse(error_msg)

        def handle_success(self, auth):
            # Now it's up to you!
            return HttpResponse('It worked!')
    return_ = Return.as_view()

`handle_success()` gives you a `tweepy.OAuth` object containing your user's
OAuth credentials. At this point you can:

* Fetch information using the tweepy API
* Create an auth.User instance and link it to a custom twitter profile

`handle_success()` just needs to return an `HttpResponse`.

After that, just hook your custom views in your app urlconf::

    # app/urls.py
    from django.conf.urls.defaults import patterns, url

    from app.views import authorize, return_

    urlpatterns = patterns(''
        url(r'^oauth/authorize/$', authorize, name='oauth_authorize'),
        url(r'^oauth/return/$', return_, name='oauth_return'),
    )
