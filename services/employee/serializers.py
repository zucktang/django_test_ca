from rest_framework import serializers
from apps.employee.models import Employee, Position, Department, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
    

class EmployeeSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'address', 'is_manager', 'position', 'department', 'status']

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value['position'] = self._get_or_create(Position, PositionSerializer, data.get('position'))
        internal_value['department'] = self._get_or_create(Department, DepartmentSerializer, data.get('department'))
        internal_value['status'] = self._get_or_create(Status, StatusSerializer, data.get('status'))
        return internal_value

    def _get_or_create(self, model, serializer_class, data):
        if isinstance(data, dict):
            missing_fields = ''
            serializer = serializer_class(data=data)
            if not serializer.is_valid(raise_exception=False):
                missing_fields = {
                    field: "This field is required."
                    for field, error in serializer.errors.items()
                    if "required" in str(error).lower()
                }
                model_key = model.__name__.lower()
            if missing_fields:
                raise serializers.ValidationError({model_key:missing_fields})
            
            obj = model.objects.filter(**data).first()
            if obj:
                return obj
            return model.objects.get_or_create(**serializer.validated_data)[0]

        elif isinstance(data, int) or isinstance(data, str):
            obj = model.objects.filter(id=data).first()
            if obj:
                return obj
            else:
                raise serializers.ValidationError({model.__name__.lower(): 'Invalid ID'})
        else:
            return None

    def get_position(self, obj):
        if obj.position:
            return PositionSerializer(obj.position).data
        return None

    def get_department(self, obj):
        if obj.department:
            return DepartmentSerializer(obj.department).data
        return None

    def get_status(self, obj):
        if obj.status:
            return StatusSerializer(obj.status).data
        return None
