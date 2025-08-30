from django.urls import path

from api.v1.customer import views
app_name = 'customer'


urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/',views.register,name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('searchby/category/',views.serach_eventby_category,name='search'),
    path('events/list/',views.events_list,name="events"),
    path("bookings/<int:id>/",views.create_booking, name="create_booking"),
    path("view/all/booking",views.View_all_booking,name="view_booking"),
    path('wishlist/add/<int:id>/', views.add_wish_list, name='add_to_wishlist'),

    


]