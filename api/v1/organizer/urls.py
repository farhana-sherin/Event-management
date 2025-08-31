from django.urls import path

from api.v1.organizer import views
app_name = 'organizer'


urlpatterns = [
    path("register/",views.register_organizer,name="register"),
    path("event/list/",views. my_events,name="event"),
    path('events/detail/<int:id>/', views.event_detail_organizer, name='event_detail'),
    path("event/create",views.create_event,name="createEvent"),
    path("event/update/<int:id>/",views.update_event,name="updateEvent"),
    path("event/delete/<int:id>/",views.delete_event,name="deleteeEvent"),
    path("logout/",views.logout,name="logout"),

   

]