from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('addtrip', views.add),
    path('create_trip', views.create),
    path('view_trip/<int:tripId>', views.view_trip),
    path('cancel/<int:planID>', views.cancel),
    path('delete/<int:id>', views.delete),
    path('join/<int:user_id>/<int:tripID>', views.join_trip),
    path('logout', views.logout),
]