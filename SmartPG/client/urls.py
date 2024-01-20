from django.urls import path
from client import client_views


urlpatterns = [
    path('home_page/', client_views.home_page),
    path('client_login/', client_views.client_login),
    path('client_forgot_password/', client_views.client_forgot_password),
    # path('client_sendmail/', client_views.Send_OTP),
    path('reset_password/', client_views.set_password),
    path('registration_show/', client_views.registration_show),
    path('client_registration/', client_views.client_registration),
    path('hostel_view/', client_views.hostel_view),
    path('user_booking/', client_views.user_booking),
    path('hostel_page/<int:id>', client_views.hostel_page),
    path('client_logout/', client_views.client_logout),
    path('owner_logout/', client_views.owner_logout),
    path('user_dashboard/', client_views.user_dashboard),
    path('feedback_insert/', client_views.feedback_insert),
    path('client_header/', client_views.client_header),
    path('client_edit/', client_views.client_edit),
    path('client_update/', client_views.client_update),
    path('client_header_menu/',client_views.load_menu),
    path('display_pg/',client_views.display_pg),
    path('booking_insert/', client_views.booking_insert),
    path('wishlist/', client_views.wishlist_show),
    path('insert_wishlist/', client_views.insert_wishlist),
    path('wish_delete/<int:id>', client_views.wish_delete),
    path('area_pg/<int:id>', client_views.area_pg),
    path('list_view/', client_views.list_view),
    path('client_inquiry/', client_views.client_inquiry),
    path('insert_inquiry/', client_views.insert_inquiry),
    path('partner_dashboard/', client_views.partner_dashboard),
    path('order_dashboard/', client_views.order_dashboard),
    path('inbox_dashboard/', client_views.inbox_dashboard),
    path('manage_dashboard/', client_views.manage_dashboard),
    path('withdraw/', client_views.withdraw),
    path('sort_hostel/',client_views.sort_data),
    path('hostel_sort/',client_views.data_sort),
    path('filter_product/', client_views.price_filter)




]