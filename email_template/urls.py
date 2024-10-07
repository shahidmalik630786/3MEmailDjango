from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path("email", views.email, name="email"),
    path("template", views.template, name="template"),
    path("template/update", views.template_update, name="template_update"),
    path("template/api", views.Template.as_view()),
    path("template/data/api", views.Template.as_view()),
    path("template/update/api", views.Template.as_view()),
    path("email/sender/api", views.EmailSender.as_view()),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)