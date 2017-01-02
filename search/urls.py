from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url
from views import Search

urlpatterns = [
                url(r'^search/$',
                    csrf_exempt(Search.as_view())),   
        ]