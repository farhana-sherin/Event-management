from django.urls import path

from api.v1.organizer import views
app_name = 'organizer'


urlpatterns = [
    path("event/list/",views.list_event,name="event"),
    path("event/create",views.create_event,name="createEvent"),
    path("event/update/<int:id>/",views.update_event,name="updateEvent"),
    path("event/delete/<int:id>/",views.delete_event,name="deleteeEvent"),

   

]