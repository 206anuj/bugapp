
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('report_bug/', views.report_bug, name="report_bug"),
    path('bug_list/', views.bug_list, name="bug_list"),
    path('download-bug-list-excel/', views.download_bug_list_excel, name='download_bug_list_excel'),
]