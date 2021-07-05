from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
import sys

class AutoLogout:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("autologout runs", file=sys.stderr)
        if request.user.is_authenticated :
            print("i am authenticated.", file=sys.stderr)
            try:
                if datetime.now() - request.session['last_touch'] > timedelta(seconds=settings.AUTO_LOGOUT_DELAY * 60):

                    print("logging out", file=sys.stderr)
                    auth.logout(request)
                    # for the expiration thingy, so we can inform the user "session is expired. please log in"

                    print("setting just expired")
                    request.session['just_expired'] = 0 
                    print("finished setting justexpired")
            except KeyError:
                print("key error - autolog out", file=sys.stderr)
        
        
        print("setting last touch", file=sys.stderr)
        request.session['last_touch'] = datetime.now()

        response = self.get_response(request)
    
        return response

class CheckExpired:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.session['just_expired'] += 1
            if request.session['just_expired'] > 1:
                del request.session['just_expired']
        except KeyError:
            pass

        response = self.get_response(request)
    
        return response

