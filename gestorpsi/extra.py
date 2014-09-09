# -*- coding: utf-8 -*-

class UserTracebackMiddleware(object):

    """
        Adds user to request context during request processing, so that they
        show up in the error emails.
    """
    
    def process_exception(self, request, exception):
        if request.user.is_authenticated():
            log = str(request.user.username)
            log += ';  '
            # maybe administrator
            try:
                log += str(request.user.get_profile().org_active)
                log += ';  '
                log += str(request.user.get_profile().org_active.id)
            except:
                pass
            request.META['AUTH_USER'] = log
        else:
            request.META['AUTH_USER'] = "Anonymous User"
