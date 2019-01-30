from django.conf.urls import include, url


urlpatterns = [url(r"^", include("rest_email_auth.urls"))]
