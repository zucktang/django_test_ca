import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apps.employee.models import (
    Employee,
    Position,
    Department,
    Status,
)
from apps.employee.factories import (
    EmployeeFactory, 
    PositionFactory, 
    DepartmentFactory, 
    StatusFactory
)
from apps.user.factories import UserFactory
from apps.user.factories import TokenFactory 



class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.position = PositionFactory(name="Developer")
        self.department = DepartmentFactory(name="IT")
        self.status = StatusFactory(name="Active")
        self.employee = EmployeeFactory(name="John Doe", position=self.position, department=self.department, status=self.status)

    def test_001_get_employee_list(self):
        response = self.client.get('/api/employee/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_002_get_employee_detail(self):
        response = self.client.get(f'/api/employee/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Doe")

    def test_003_create_employee(self):
        data = {
            "name": "Jane Doe",
            "address": "Test Address",
            "manager": False,
            "position": self.position.id,
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_004_update_employee(self):
        data = {
            "name": "John Updated",
            "address": "Test Address",
            "manager": True,
            "position": self.position.id,
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.put(f'/api/employee/{self.employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "John Updated")
        
    def test_005_patch_employee(self):
        # Test partial update with PATCH
        data = {
            "address": "Patched Address",
            "is_manager": False,
        }
        response = self.client.patch(f'/api/employee/{self.employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.address, "Patched Address")
        self.assertFalse(self.employee.is_manager)

    def test_006_delete_employee(self):
        response = self.client.delete(f'/api/employee/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
        
    
    def test_007_create_employee_with_invalid_data(self):
        data = {
            "name": "Invalid Employee",
            "address": "Test Address",
            "is_manager": False,
            "position": 99999, 
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('position', response.data)
        
    def test_008_create_employee_with_dict_for_position(self):
        data = {
            "name": "New Manager",
            "address": "New Manager Address",
            "is_manager": True,
            "position": {
                "name": "Manager",
                "salary": 1800000
            },
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(name="New Manager").position.name, "Manager")

    def test_009_create_employee_with_dict_for_department(self):
        data = {
            "name": "New Employee",
            "address": "New Emplpyee Address",
            "is_manager": False,
            "position": self.position.id,
            "department": {
                "name": "BKK",
            },
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(name="New Employee").department.name, "BKK")

    def test_010_create_employee_with_dict_for_status(self):
        data = {
            "name": "New Employee",
            "address": "New Emplpyee Address",
            "is_manager": True,
            "position": self.position.id,
            "department": self.department.id,
            "status": {
                "name": "Inactive", 
                
            },
        }
        response = self.client.post('/api/employee/', data, 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.get(name="New Employee").status.name, "Inactive")
        
    def test_011_create_employee_with_missing_salary_for_position_dict(self):
        data = {
            "name": "New Manager",
            "address": "New Manager Address",
            "is_manager": True,
            "position": {
                "name": "Manager",
            },
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data, 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"position": {"salary": "This field is required."}})
        
    def test_012_create_employee_with_missing_name_for_position_dict(self):
        data = {
            "name": "New Manager",
            "address": "Test Address",
            "is_manager": False,
            "position": {
                "salary": 1800000,
            },
            "department": self.department.id,
            "status": self.status.id,
        }
        response = self.client.post('/api/employee/', data, 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"position": {"name": "This field is required."}})
        
class StatusAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.status = StatusFactory(name="Active")

    def test_001_get_status_list(self):
        response = self.client.get('/api/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_002_get_status_detail(self):
        response = self.client.get(f'/api/status/{self.status.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Active")

    def test_003_create_status(self):
        data = {"name": "Inactive"}
        response = self.client.post('/api/status/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)

    def test_004_update_status(self):
        data = {"name": "Pending"}
        response = self.client.put(f'/api/status/{self.status.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Pending")

    def test_005_delete_status(self):
        response = self.client.delete(f'/api/status/{self.status.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Status.objects.count(), 0)
        
    def test_006_patch_status_name(self):
        data = {"name": "Archived"}
        response = self.client.patch(f'/api/status/{self.status.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Archived")

class DepartmentAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.department = DepartmentFactory(name="IT")

    def test_001_get_department_list(self):
        response = self.client.get('/api/department/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_002_get_department_detail(self):
        response = self.client.get(f'/api/department/{self.department.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "IT")

    def test_003_create_department(self):
        data = {"name": "HR"}
        response = self.client.post('/api/department/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 2)

    def test_004_update_department(self):
        data = {"name": "IT"}
        response = self.client.put(f'/api/department/{self.department.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "IT")

    def test_005_delete_department(self):
        response = self.client.delete(f'/api/department/{self.department.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Department.objects.count(), 0)
        
    def test_006_patch_department_name(self):
        data = {"name": "Operations"}
        response = self.client.patch(f'/api/department/{self.department.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "Operations")

class PositionAPITestCase(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.position = PositionFactory(name="Developer")

    def test_001_get_position_list(self):
        response = self.client.get('/api/position/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_002_get_position_detail(self):
        response = self.client.get(f'/api/position/{self.position.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Developer")

    def test_003_create_position(self):
        data = {"name": "Manager", "salary": 75000}
        response = self.client.post('/api/position/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Position.objects.count(), 2)

    def test_004_update_position(self):
        data = {"name": "Lead Developer", "salary": 85000}
        response = self.client.put(f'/api/position/{self.position.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Lead Developer")

    def test_005_delete_position(self):
        response = self.client.delete(f'/api/position/{self.position.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Position.objects.count(), 0)
        
    def test_006_patch_position_name(self):
        data = {"name": "Senior Developer"}
        response = self.client.patch(f'/api/position/{self.position.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Senior Developer")

    def test_007_patch_position_salary(self):
        data = {"salary": 80000}
        response = self.client.patch(f'/api/position/{self.position.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.position.refresh_from_db()
        self.assertEqual(self.position.salary, 80000)