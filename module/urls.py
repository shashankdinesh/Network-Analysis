from django.conf.urls import url
from .views import dataset_mp_api,dataset_route,dataset_set_mp_new,dataset_set_mp_new_bifurcated

urlpatterns = [
url('pythonurl/service/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)', dataset_mp_api, name='dataset_mp_api'),
url('wine', dataset_set_mp_new_bifurcated, name='wine')
    ]
