from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import EmployeeViewSet, PositionViewSet, DepartmentViewSet, StatusViewSet

router = DefaultRouter()
router.register(r'position', PositionViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'status', StatusViewSet)
router.register(r'employee', EmployeeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]