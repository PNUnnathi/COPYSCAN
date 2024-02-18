from django import views
from django.urls import path
#from ..edits.registration.views2 import authView, file_upload_view, home, ResetPasswordView, text_input_view,text_page
from django.contrib.auth import views as auth_views

from  base.middlewares.auth import auth_middleware
from  base.views2.doc import file_upload_view
from  base.views2.imageplag import image_upload_view
#from  base.views2.image import image_search


from  .views import Paraphrase, TextInputView, TextSaveView, download_pdf,  home,  text_page
from .views2.signup import Signup
from .views2.login import Login , logout


app_name = 'base'

urlpatterns = [
   path('',home,name="home"),
   #path("signup/",authView,name="authView"),
   #path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
   path('text_page/', text_page, name='text_page'),
   path('submit/', TextInputView.as_view(), name='submit'),
   path('file/', file_upload_view, name='file_upload'),
   #path("accounts/", include("django.contrib.auth.urls")),
   path('image/', image_upload_view,name='image_search'),
   path('signup2', Signup.as_view(), name='signup'),
   path('login2', Login.as_view(), name='login2'),
   path('logout', logout , name='logout'),
   path('result', auth_middleware(TextSaveView.as_view()), name='result'),
   path('paraphrase/', Paraphrase.as_view(), name='paraphrase'),
   path('download_pdf/', download_pdf, name='download_pdf'),
]
