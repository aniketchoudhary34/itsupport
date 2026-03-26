from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns=[
    
    path('help',views.baseview,name='base'),
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_view,name='register'),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('update_profile/<int:pk>/', views.update_profile, name='update_profile'),
    path('taskdetails/', views.create_task, name='create_task'),

    path('task_info/<int:pk>/', views.task_info, name='task_info'),
    path('update_task/<int:pk>/', views.update_task, name='update_task'),
    path('deletetask/<int:pk>/', views.deletetask, name='deletetask'),
    path('mycart/', views.mycarts, name='mycart'),
    path('accept_task/<int:pk>/', views.accept_task, name='accept_task'),
    path('remove_task/<int:pk>/', views.remove_task, name='remove_task'),
    path('mark_done/<int:pk>/', views.mark_done, name='mark_done'),
    path('add_user/', views.add_user, name='add_user'),
    path('user_list/', views.user_list, name='user_list'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('toggle_user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("update-role/<int:user_id>/", views.update_user_role, name="update_user_role"),
    path('close_task/<int:pk>/', views.close_task, name='close_task'),
    path("report/", views.report_criteria),

    path("report/criteria/", views.report_criteria, name="report_criteria"),
    path("reports/view/", views.report_view, name="report_view"),
    path("reports/download/", views.report_download, name="report_download"),


    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
