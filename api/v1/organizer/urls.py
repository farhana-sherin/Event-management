from django.urls import path

from api.v1.organizer import views
app_name = 'organizer'


urlpatterns = [
    path("event/list/",views.list_event,name="event"),
   

]