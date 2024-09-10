from services.core import viewsets, permissions
from apps.employee.models import Employee, Position, Department, Status
from .serializers import EmployeeSerializer, PositionSerializer, DepartmentSerializer, StatusSerializer
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['position', 'department', 'status']
    search_fields = ['name', 'address']
    ACTION_SERIALIZERS = {
        'list': EmployeeSerializer, 
        'retrieve': EmployeeSerializer,
        'create': EmployeeSerializer,
        'update': EmployeeSerializer,
        'partial_update': EmployeeSerializer,
        'destroy': EmployeeSerializer,
    }

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ACTION_SERIALIZERS = {
        'list': PositionSerializer, 
        'retrieve': PositionSerializer,
        'create': PositionSerializer,
        'update': PositionSerializer,
        'partial_update': PositionSerializer,
        'destroy': PositionSerializer,
    }

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ACTION_SERIALIZERS = {
        'list': DepartmentSerializer, 
        'retrieve': DepartmentSerializer,
        'create': DepartmentSerializer,
        'update': DepartmentSerializer,
        'partial_update': DepartmentSerializer,
        'destroy': DepartmentSerializer,
    }

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    ACTION_SERIALIZERS = {
        'list': StatusSerializer, 
        'retrieve': StatusSerializer,
        'create': StatusSerializer,
        'update': StatusSerializer,
        'partial_update': StatusSerializer,
        'destroy': StatusSerializer,
    }
    