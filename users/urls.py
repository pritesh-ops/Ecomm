from django.urls import path
from . import views

app_name = 'users'  # Add this for namespace support

urlpatterns = [
    # Authentication URLs
    path("login/", views.Login.as_view(), name="login"),
    path("signup/", views.Register.as_view(), name="signup"),
    path("logout/", views.logout_view, name="logout"),
    
    # Profile Management URLs
    path("profile/", views.Profile.as_view(), name="profile"),
    
    # Address Management URLs
    path("address/save/", views.SaveAddress.as_view(), name="save_address"),
    path("address/edit/<int:address_id>/", views.EditAddress.as_view(), name="edit_address"),
    path("address/delete/<int:address_id>/", views.DeleteAddress.as_view(), name="delete_address"),

    # Additional user-related URLs can be added here
    # Example:
    # path("settings/", views.AccountSettings.as_view(), name="account_settings"),
]