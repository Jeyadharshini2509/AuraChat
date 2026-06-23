from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat_home, name="chat_home"),
    path("thread/<int:thread_id>/", views.chat_thread, name="chat_thread"),
    path("send/", views.send_message, name="send_message"),
    path("thread/<int:thread_id>/delete/", views.delete_thread, name="delete_thread"),
    path("signup/", views.signup, name="signup"),
]
