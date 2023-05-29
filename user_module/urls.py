from user_module import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from .views import initiate_payment, payment_callback

app_name = 'user_module'

router = DefaultRouter()
router.register('booking', views.BookingViewSet, basename='booking')

urlpatterns = [
    path('login_api/', views.LoginView.as_view(), name='login_api'),
    path('logout/', views.logout_page, name='logout_page'),
    path('signup/', views.sign_up, name='sign_up'),
    path('signup_api/', views.SignUpView.as_view(), name='signup_api'),
    path('home/', views.home, name='home'),
    path('login/', views.login_page, name='login_page'),

    path('', include(router.urls)),
    path('booking-list/', views.booking_list, name='booking_list'),
    path('booking-payment-update/', views.booking_payment_update, name='booking_payment_update'),

    path('download-charts/', views.download_charts_as_pdf, name='download_charts'),
    path('send-otp-email/', views.send_otp_email, name='send_otp_email'),

    path('get_context_data/', views.BookingViewSet.as_view({'get': 'get_context_data'}), name='get_context_data'),
    path('admin-module/download-bookings-excel/', views.download_bookings_excel, name='download_bookings_excel'),

    # payment process

    path('payment/proceed/', views.proceed_payment, name='proceed_payment'),

]
