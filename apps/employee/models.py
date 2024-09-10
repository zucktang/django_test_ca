from django.db import models

from .abstract_models import (
    AbstractDepartment,
    AbstractEmployee,
    AbstractPosition,
    AbstractStatus,
)

class Employee(AbstractEmployee):
    pass

class Department(AbstractDepartment):
    pass

class Position(AbstractPosition):
    pass

class Status(AbstractStatus):
    pass
