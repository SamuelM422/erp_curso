from django.urls import path
from accounts.views.signin import Signin
from accounts.views.signup import Signup

app_name = 'accounts'

urlpatterns = [
    path('auth/', lambda request: ..., name='auth'),
    path('auth/signin/', Signin.as_view(), name='signin'),
    path('auth/signup/', Signup.as_view(), name='signup'),
]