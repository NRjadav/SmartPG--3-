"""smartpg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Admin import views
from client import client_views
import django.urls as  url
from Admin.views import HomeView, projectChart
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('view/', views.view),
    path('admin_edit/', views.admin_edit),
    path('admin_update/', views.admin_update),
    path('area/', views.area_show),
    path("edit/<int:area_id>", views.edit),
    path("update/<int:id>", views.update),
    path('pgdetails/', views.pgdetails_show),
    path('pgdetails_insert/', views.pgdetails_insert),
    path('pgdetails_edit/<int:pg_id>', views.pgdetails_edit),
    path('pgdetails_update/<int:pg_id>', views.pgdetails_update),
    path('bookingdetails_show/', views.bookingdetails_show),
    path('facility/', views.facility_show),
    path('facility_edit/<int:facility_id>', views.facility_edit),
    path('facility_update/<int:facility_id>', views.facility_update),
    path('feedback_show/', views.feedback_show),
    path('feedback_insert/', views.feedback_insert),
    path('feedback_edit/<int:feedback_id>', views.feedback_edit),
    path('feedback_delete/<int:feedback_id>', views.feedback_delete),
    path('gallery_show/', views.gallery_show),
    path('gallery_insert/', views.gallery_insert),
    path('inquiry/', views.inquiry_show),
    path('pgowner_show/', views.pgowner_show),
    path('pgfacility_show/', views.pgfacility_show),
    path('pgfacility_show/<int:id>', views.pgfacility_show),
    path('forgot/', views.forgot_password),
    path('sendmail/', views.Send_OTP),
    path('delete/<int:id>', views.delete),
    path('facility_delete/<int:facility_id>', views.facility_delete),
    path('pgdetails_delete/<int:pg_id>', views.pgdetails_delete),
    path('gallery_delete/<int:gallery_id>', views.gallery_delete),
    path('area_insert/', views.area_insert),
    path('facility_insert/', views.facility_insert),
    path('bookingdetails1/', views.bookingdetails1),
    path('bookingdetails2/', views.bookingdetails2),
    path('customer_count_report/', views.customer_count_report),
    path('data/', views.data),
    path('login/', views.admin_login),


    path('reset_pass/', views.set_password),
    path('index/', views.index),

    path("accept/<int:booking_id>", views.accept),
    path("reject/<int:booking_id>", views.reject),
    path("logout/", views.logout),
    path('', client_views.client_login),

    # url(r'charthome', HomeView.as_view(), name='home'),
    # url(r'^api/chart/data/$', projectChart.as_view(), name="api-data"),

    path('client/', include('client.urls')),
    path('pgowner/', include('pgowner.urls')),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)