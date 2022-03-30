import base64

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from functools import wraps
# def view_or_basicauth(view, request, test_func, realm = "", *args, **kwargs):
#     """
#     This is a helper function used by both 'logged_in_or_basicauth' and
#     'has_perm_or_basicauth' that does the nitty of determining if they
#     are already logged in or if they have provided proper http-authorization
#     and returning the view if all goes well, otherwise responding with a 401.
#     """
#     if test_func(request.user):
#         # Already logged in, just return the view.
#         #
#         return view(request, *args, **kwargs)

#     # They are not logged in. See if they provided login credentials
#     print(request.META)
#     print(request.headers)
#     if 'HTTP_AUTHORIZATION' in request.META:
#         auth = request.META['HTTP_AUTHORIZATION'].split()
#         if len(auth) == 2:
#             # NOTE: Wevonly support basic authentication for now.
#             #
#             if auth[0].lower() == "basic":
#                 uname, passwd = base64.b64decode(auth[1]).split(':')
#                 user = authenticate(username=uname, password=passwd)
#                 if user is not None:
#                       login(request, user)
#                       request.user = user
#                       return view(request, *args, **kwargs)

#     # Either they did not provide an authorization header or
#     # something in the authorization attempt failed. Send a 401
#     # back to them to ask them to authenticate.
#     #
#     response = HttpResponse()
#     response.status_code = 401
#     response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
#     return response

# def view_or_basicauth(function):
#   @wraps(function)
#   def wrap(request, *args, **kwargs):
#     print(request.META)
#     print(request.headers)
#     if 'HTTP_AUTHORIZATION' in request.META:
#         auth = request.META['HTTP_AUTHORIZATION'].split()
#         if len(auth) == 2:
#             if auth[0].lower() == "basic":
#                 uname, passwd = base64.b64decode(auth[1]).split(':')
#                 user = authenticate(username=uname, password=passwd)
#                 if user is not None:
#                       login(request, user)
#                       request.user = user
#                       return function(request, *args, **kwargs)

#     response = HttpResponse()
#     response.status_code = 401
#     return response

#   return wrap

def view_or_basicauth():
  def decorator(func):
    def wrapper(request, *args, **kwargs):
      print(request.META)
      if 'HTTP_AUTHORIZATION' in request.META:
          auth = request.META['HTTP_AUTHORIZATION'].split()
          if len(auth) == 2:
              if auth[0].lower() == "basic":
                  uname, passwd = base64.b64decode(auth[1]).decode('utf-8').split(':')
                  user = authenticate(username=uname, password=passwd)
                  if user is not None:
                        request.user = user
                        return func(request, *args, **kwargs)

      response = HttpResponse()
      response.status_code = 401
      return response
    return wrapper
  return decorator
