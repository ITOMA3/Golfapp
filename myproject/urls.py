
# urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from GolfApp import views
from GolfApp.views import ParticipantCreateView
from GolfApp.views import ParticipantUpdateView


urlpatterns = [
    path('', views.index, name='index'),
    path('group_results/', views.group_results, name='group_results'),
    path('register/', views.ParticipantCreateView.as_view(), name='participant_register'),
    path('delete/', views.show_delete_participants_form, name='show_delete_participants_form'),
    path('delete_participants/', views.delete_participants, name='delete_participants'),
    path('participant/edit/<int:pk>/', ParticipantUpdateView.as_view(), name='participant_edit'),

]  # 他のURLパターン...
