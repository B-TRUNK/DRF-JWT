from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),                     # your app
    path("api-auth/", include("rest_framework.urls")), # browsable API login
    # Simple JWT
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]