from django.urls import include, path


urlpatterns = [path(r"", include("rest_email_auth.urls"))]
