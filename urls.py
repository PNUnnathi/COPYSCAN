from django import views
from django.urls import path
#from ..edits.registration.views2 import authView, file_upload_view, home, ResetPasswordView, text_input_view,text_page
from django.contrib.auth import views as auth_views

from  base.middlewares.auth import auth_middleware
from  .views2.paraphrase import ParaphraseTextView

from  .views import TextSaveView, TextInputView, file_upload_view, home,  text_page
from .views2.signup import Signup
from .views2.login import Login , logout



urlpatterns = [
   path('',home,name="home"),
   #path("signup/",authView,name="authView"),
   #path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
   path('text_page/', text_page, name='text_page'),
   path('submit/', TextInputView.as_view(), name='submit'),
   path('file/', file_upload_view, name='file_upload'),
   #path("accounts/", include("django.contrib.auth.urls")),
 
   
   path('signup2', Signup.as_view(), name='signup'),
   path('login2', Login.as_view(), name='login2'),
   path('logout', logout , name='logout'),
   path('result', auth_middleware(TextSaveView.as_view()), name='result'),
   path('paraphrase', ParaphraseTextView.as_view(), name='paraphrase_text')
]
