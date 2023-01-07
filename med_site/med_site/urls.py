import django.contrib.admin
from django.contrib import admin
from django.urls import path
from homepage.views import *

urlpatterns = [
    path("", homepage, name="homepage"),
    path("doctors", doctors, name="doctors"),
    path("doctors/<str:profes>", doctors, name="doctor"),
    path("customers", customers, name="customers"),
    path("timetable", timetable, name="timetable"),
    path("generate", generate, name="generate"),
    path("login", sign, name="login"),
    path("logout", logout_user, name="logout"),
    path("admin", admin.site.urls),
    path("appointment/<str:profes>/<int:id>", appointment, name='appointment'),
    path("dwlpdf", download_pdf, name="dwlpdf"),
    path("dwlcsv", download_csv, name="dwlcsv"),
    path("new_doc", new_doctor, name="new_doc"),
    path("change_diganosis/<int:id>", change_diganosis, name="change_diganosis")
]