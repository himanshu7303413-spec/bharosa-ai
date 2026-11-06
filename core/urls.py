from django.urls import path
from . import views as v
urlpatterns = [path("", v.dashboard, name="dashboard"), path("gateway/", v.gateway, name="gateway"),
    path("redteam/", v.redteam, name="redteam"), path("dpdp/", v.dpdp, name="dpdp"), path("kagaz/", v.kagaz, name="kagaz"),
    path("health/", v.health, name="health"), path("api/gateway/", v.api_gateway, name="api_gateway")]
