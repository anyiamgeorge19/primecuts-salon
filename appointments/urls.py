from django.urls import path
from . import views

app_name = "appointments"
urlpatterns = [
    path("stylists/", views.stylist_list, name="stylist_list"),
    path("stylists/<int:pk>/", views.stylist_detail, name="stylist_detail"),
    path("book/", views.book_appointment, name="book_appointment"),
    path("available-slots/", views.available_slots, name="available_slots"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("cancel/<int:pk>/", views.cancel_appointment, name="cancel_appointment"),
    path("dashboard/", views.stylist_dashboard, name="stylist_dashboard"),
    path("update-status/<int:pk>/<str:new_status>/", views.update_status, name="update_status"),
]
