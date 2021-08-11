from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.index),
    path('dashboard', views.dashboard),
    path('jobs/new', views.display_add_job),
    path('jobs/<int:job_id>', views.display_one_job),
    path('jobs/edit/<int:job_id>', views.display_edit_job),

    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('jobs/<int:job_id>/destroy', views.destroy_job),
    path('jobs/<int:job_id>/update', views.update_job),
    path('jobs/add_job', views.add_job),
]