from companies.views.base import Base
from companies.utils.permissions import DynamicPermission
from companies.utils.decorators import dynamic_permission
from companies.models import Employee, Enterprise
from companies.serializers import EmployeeSerializer, EmployeesSerializer
from accounts.auth import Authentication
from accounts.models import User, UserGroups
from rest_framework.views import Response
from rest_framework import status
from rest_framework.exceptions import APIException

@dynamic_permission(permission_to='employee')
class Employees(Base):
    permission_classes = [DynamicPermission]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)

        owner_id = Enterprise.objects.values('user_id').filter(id=enterprise_id).first()['user_id']

        employees = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner_id).all()

        serializer = EmployeesSerializer(employees, many=True)

        return Response({
            'employees': serializer.data,
        })

    def post(self, request):
        data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'company_id': self.get_enterprise_id(request.user.id),
            'type_account': 'employee',
        }

        Authentication.signup(**data)

        return Response({'success': True }, status = status.HTTP_201_CREATED)


@dynamic_permission(permission_to='employee')
class EmployeeDetail(Base):
    permission_classes = [DynamicPermission]

    def get(self, request, employee_id):
        employee = self.get_employee(employee_id, request.user.id)

        serializer = EmployeeSerializer(employee)

        return Response({
            'employee': serializer.data,
        })

    def put(self, request, employee_id):
        ...