from django.urls import path
from django.conf import settings
from  django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),
    path('/', views.index),
    path('students/', views.students),
    path('notifications/', views.notifications),
    path('account/', views.account, name='account'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('find-student/', views.find_student, name='find_student'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('add/', views.add, name='add'),
]