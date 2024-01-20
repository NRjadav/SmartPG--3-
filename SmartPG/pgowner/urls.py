from django.urls import path
from pgowner import pgowner_views


urlpatterns = [
    path('pg_index/', pgowner_views.pg_index),
    path('report1/', pgowner_views.bookingdetails2),
    path('report2/', pgowner_views.bookingdetails1),
    path('owner_edit/', pgowner_views.owner_edit),
    path('owner_update/', pgowner_views.owner_update),
    path('owner_login/', pgowner_views.owner_login),
    path('owner_registration/', pgowner_views.owner_registration),
    path('owner_pgowner/', pgowner_views.owner_pgowner),
    path('owner_pgmenu/', pgowner_views.owner_pgmenu),
    path('owner_gallery/', pgowner_views.owner_gallery),
    path('gallery_ins/', pgowner_views.gallery_ins),
    path('user_view/', pgowner_views.user_view),
    path('owner/', pgowner_views.owner),
    path('owner_area/', pgowner_views.owner_area),
    path('owner_facility/', pgowner_views.owner_facility),
    path('owner_pgfacility/', pgowner_views.owner_pgfacility),
    path('owner_pgfacility/<int:id>', pgowner_views.owner_pgfacility),
    path('owner_feedback/', pgowner_views.owner_feedback),
    path('owner_feedback_insert/', pgowner_views.owner_feedback_insert),
    path('owner_feedback_edit/<int:feedback_id>', pgowner_views.owner_feedback_edit),
    path('owner_feedback_update/<int:feedback_id>', pgowner_views.owner_feedback_update),
    path('owner_bookingdetails/', pgowner_views.owner_bookingdetails),
    path('owner_inquiry/', pgowner_views.owner_inquiry),
    path('count_report/', pgowner_views.count_report),
    path('owner_pgdetails_insert/', pgowner_views.owner_pgdetails_insert),
    path('owner_pgmenu_insert/', pgowner_views.owner_pgmenu_insert),
    path('owner_pgdetails_edit/<int:pg_id>', pgowner_views.owner_pgdetails_edit),
    path('owner_pgdetails_update/<int:pg_id>', pgowner_views.owner_pgdetails_update),
    path('owner_logout/', pgowner_views.owner_logout),
    path('owner_forgot_password/', pgowner_views.owner_forgot_password),
    path('pass_reset/', pgowner_views.set_password),
    path('owner_sendmail/', pgowner_views.Send_OTP),
    path('pgdetails_delete/<int:pg_id>', pgowner_views.pgdetails_delete),
    path('pgdetails_delete/<int:pg_id>', pgowner_views.pgdetails_delete),


]
