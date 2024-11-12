from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

api_urls = [  # Tried to figure out why http://127.0.0.1:8000/api/?format=api shows cut endpoints with no success
    path("", include("tasks.urls")),
    path("", include("users.urls")),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
]
