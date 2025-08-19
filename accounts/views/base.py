from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from companies.models import Enterprise, Employee
from accounts.models import UserGroups, GroupPermissions

class Base(APIView):
    @staticmethod
    def get_enterprise_user(user_id):
        enterprise  = {'is_owner': Enterprise.objects.filter(user_id=user_id).exists(), 'permissions': []}

        if enterprise['is_owner']: return enterprise

        employee = Employee.objects.filter(user_id=user_id).first()

        if not employee: raise APIException('User is not an employee')

        groups = UserGroups.objects.filter(user_id=user_id).all()

        for g in groups:
            group = g.group

            permissions = GroupPermissions.objects.filter(group_id=group.pk).all()

            for p in permissions:
                enterprise['permissions'].append({
                    'id': p.permission.id,
                    'label': p.permission.name,
                    'codename': p.permission.codename
                })

        return enterprise