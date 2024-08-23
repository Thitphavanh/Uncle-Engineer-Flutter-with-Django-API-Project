from django.http import JsonResponse
from .models import Maintenance
from .serializers import MaintenanceSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import generics
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def maintenance_api(request):
    maintenances = Maintenance.objects.all()
    serializer = MaintenanceSerializer(maintenances, many=True)
    return JsonResponse(
        {
            "data": serializer.data,
        }
    )


# @authentication_classes([])
# @permission_classes([])
# def maintenance_detail_api(request, mid):
#     try:
#         maintenances = Maintenance.objects.get(id=mid)
#         serializer = MaintenanceSerializer(maintenances)
#     except:
#         return redirect("maintenance-api")
#     return JsonResponse(serializer.data, json_dumps_params={"ensure_ascii": False})


@api_view(["GET"])
def maintenance_get_api(request, mid):
    maintenances = Maintenance.objects.get(id=mid)
    if request.method == "GET":
        serializer = MaintenanceSerializer(maintenances)
        return Response(serializer.data)


@api_view(["POST"])
def maintenance_post_api(request):
    if request.method == "POST":
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def maintenance_update_api(request, mid):
    try:
        # Retrieve the Maintenance instance by id
        maintenances = get_object_or_404(Maintenance, id=mid)
        # Initialize the serializer with the existing instance and new data
        serializer = MaintenanceSerializer(maintenances, data=request.data)

        # Validate and save the updated data
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data["message"] = "ข้อมูลอัปเดตใหม่"
            return Response(
                data, status=status.HTTP_200_OK
            )  # Use 200 OK for successful updates

        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Use 400 for bad request

    except Maintenance.DoesNotExist:
        return Response(
            {"error": "Maintenance not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # if request.method == "PUT":
    #     maintenances = Maintenance.objects.get(id=mid)
    #     serializer = MaintenanceSerializer(maintenances, data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     data = serializer.data
    #     data["message"] = "ข้อมูลอัปเดตใหม่"
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def maintenance_delete_api(request, mid):
    if request.method == "DELETE":
        maintenances = Maintenance.objects.get(id=mid)
        deleted = maintenances.delete()
        data = {}
        if deleted:
            data["message"] = "ข้อมูลถูกลบสำเร็จแล้ว"
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data["message"] = "ข้อมูลถูกลบไม่สำเร็จ"
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)


# ----------------------------------------------------
class MaintenanceAPI(generics.ListAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

class MaintenanceGetAPI(generics.RetrieveAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

class MaintenanceCreateAPI(generics.ListCreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class MaintenanceUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class MaintenanceDeleteAPI(generics.DestroyAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
