from django.urls import path

from rentservice import views

urlpatterns = [
    path('cities/', views.CityList.as_view()),
    path('cities/<int:city_id>/', views.CityDetail.as_view()),
    path('cities/<int:city_id>/streets/', views.ApartmentDetail.as_view()),
    path('apartment/', views.ApartmentFilter.as_view()),
]
