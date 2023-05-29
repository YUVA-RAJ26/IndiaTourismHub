from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'admin_module'

router = DefaultRouter()
router.register('states', views.StateViewSet, basename='state')
router.register('districts', views.DistrictViewSet, basename='district')
router.register('tour-packages', views.TourPackageViewSet, basename='tour-package')
router.register('hotels', views.HotelViewSet, basename='hotel')
router.register('tourist-places', views.TouristPlaceViewSet, basename='tourist-place')
router.register('discountcodes', views.DiscountCodeViewSet, basename='discountcode')

urlpatterns = [
    path('tourist-list/', views.tourist_place_list, name='tourist_list'),
    path('hotel-list/', views.hotel_list, name='hotel_list'),
    path('tour-package-list/', views.tour_package_list, name='tour_package_list'),
    path('create-tourist/', views.create_tourist_place, name='create_tourist'),
    path('', include(router.urls)),
    path('districts/get_state_districts/<int:state_id>/', views.DistrictViewSet.as_view({'get': 'get_state_districts'}), name='get_state_districts'),
    path('districts/get_pincode_state_districts/', views.DistrictViewSet.as_view({'get': 'get_pincode_state_districts'}), name='get_pincode_state_districts'),
    
    path('tour-packages-pdf/', views.download_tour_packages_pdf, name='download_tour_packages_pdf'),
]
