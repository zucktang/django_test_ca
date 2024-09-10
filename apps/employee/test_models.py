from django.test import TestCase
from apps.employee.models import Employee
from .factories import EmployeeFactory, PositionFactory, DepartmentFactory, StatusFactory

class ModelTestCase(TestCase):
    
    def setUp(self):
        self.position = PositionFactory(name="Developer", salary=100000)
        self.department = DepartmentFactory(name="IT")
        self.status = StatusFactory(name="Active", )
        self.employee = EmployeeFactory(name="John Doe", position=self.position, department=self.department, status=self.status)
    
    def test_position_creation(self):
        position = PositionFactory(name="Manager", salary=120000)
        self.assertEqual(position.name, "Manager")
    
    def test_department_creation(self):
        department = DepartmentFactory(name="HR")
        self.assertEqual(department.name, "HR")
    
    def test_status_creation(self):
        status = StatusFactory(name="Inactive")
        self.assertEqual(status.name, "Inactive")
    
    def test_employee_creation(self):
        employee = Employee.objects.get(name="John Doe")
        self.assertEqual(employee.name, "John Doe")
        self.assertEqual(employee.position, self.position)
        self.assertEqual(employee.department, self.department)
        self.assertEqual(employee.status, self.status)