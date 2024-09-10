import factory
from apps.user.models import User
from apps.employee.models import Employee, Position, Department, Status


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    name = factory.Faker('job')
    salary = factory.Faker('random_number', digits=5)

class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = factory.Faker('company')

class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.Faker('word')

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    name = factory.Faker('name')
    address = factory.Faker('address')
    is_manager = False
    position = factory.SubFactory(PositionFactory)
    department = factory.SubFactory(DepartmentFactory)
    status = factory.SubFactory(StatusFactory)