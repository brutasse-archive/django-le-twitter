from django.conf import settings
from django.shortcuts import redirect
from django.views import generic

import tweepy


class Authorize(generic.View):
    """
    A base class for the authorize view. Just sets the request token
    in the session and redirects to twitter.
    """
    def get(self, request, *args, **kwargs):
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,
                                   settings.CONSUMER_SECRET, secure=True)
        url = auth.get_authorization_url(signin_with_twitter=True)
        request.session['request_token'] = (auth.request_token.key,
                                            auth.request_token.secret)
        return redirect(url)


class Return(generic.View):
    """
    A base class for the return callback. Subclasses must define:

        - handle_error(error_msg, exception=None): what to do when
          something goes wrong? Must return an HttpResponse

        - handle_success(auth): what to do on successful auth? Do
          some stuff with the tweepy.OAuth object and return
          an HttpResponse
    """
    def get(self, request, *args, **kwargs):
        verifier = request.GET.get('oauth_verifier', None)
        if verifier is None:
            return self.handle_error('No verifier code')

        if not 'request_token' in request.session:
            return self.handle_error('No request token found in the session')

        request_token = request.session.pop('request_token')
        request.session.modified = True

        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY,
                                   settings.CONSUMER_SECRET, secure=True)
        auth.set_request_token(request_token[0], request_token[1])
        try:
            auth.get_access_token(verifier=verifier)
        except tweepy.TweepError as e:
            return self.handle_error('Failed to get an access token')

        return self.handle_success(auth)

    def handle_success(self, auth):
        """
        Twitter authentication successful, do some stuff with his key.
        """
        raise NotImplementedError

    def handle_error(self, error_msg, exception=None):
        """
        Meh. Something broke.
        """
        raise NotImplementedError
