from django.urls import path

from api.v1.customer import views
app_name = 'customer'


urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/',views.register,name='register'),


]