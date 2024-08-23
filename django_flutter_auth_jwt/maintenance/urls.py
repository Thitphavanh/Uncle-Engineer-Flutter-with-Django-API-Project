from django.urls import path
from . import api
from .api import *


urlpatterns = [
    path("all-maintenance/", api.maintenance_api, name="maintenance-api"),
    path("maintenance/<int:mid>/", api.maintenance_get_api),
    path("post-maintenance/", api.maintenance_post_api),
    path("update-maintenance/<int:mid>/", api.maintenance_update_api),
    path("delete-maintenance/<int:mid>/", api.maintenance_delete_api),
    # ----------------------------------------------------
    # path("detail/<int:mid>/", api.maintenance_detail_api, name="maintenance-detail-api"),
    # path("get/<int:mid>/", api.maintenance_get_api),
    # ----------------------------------------------------
    # path("all-maintenance", MaintenanceAPI.as_view(), name="maintenance-all-api"),
    # path("maintenance/<int:pk>/", MaintenanceGetAPI.as_view(), name="maintenance-get-api"),
    # path("post-maintenance/", MaintenanceCreateAPI.as_view(), name="maintenance-create-api"),
    # path("update-maintenance/<int:pk>/", MaintenanceUpdateAPI.as_view(), name="maintenance-update-api"),
    # path("delete-maintenance/<int:pk>/", MaintenanceDeleteAPI.as_view(), name="maintenance-update-api"),
]
