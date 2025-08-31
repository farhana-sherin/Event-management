from django.urls import path

from api.v1.customer import views
app_name = 'customer'



urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/',views.register,name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path("logout/",views.logout,name="logout"),
    path('searchby/category/',views.search_events,name='search'),
    path('events/list/',views.events_list,name="events"),
    path('events/detail/<int:id>/', views.event_detail, name='event_detail'),
    path("bookings/<int:id>/",views.create_booking, name="create_booking"),
    path("booking/cancel/<int:id>/", views.cancel_booking, name="cancel_booking"),
    path("view/all/booking",views.View_all_booking,name="view_booking"),
    path('wishlist/add/<int:id>/', views.add_wish_list, name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.list_wishlist, name='list_wishlist'),
    path("notification/",views.notification,name="notification"),
    path("notification/<int:id>/", views.notification_detail, name="notification-detail"),
    path('notification/mark/read/<int:id>/',views.mark_notification_read, name='mark-notification-read'),
    path("notification/mark/read/all",views.mark_all_notifications_read,name="notification_mark_all"),
    






    


]