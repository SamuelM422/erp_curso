from rest_framework import permissions
from accounts.models import UserGroups, GroupPermissions

def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False

    if user.is_owner:
        return True

    match method:
        case 'POST':
            required_permission = 'add_' + permission_to
        case 'PUT':
            required_permission = 'change_' + permission_to
        case 'DELETE':
            required_permission = 'delete_' + permission_to
        case _:
            required_permission = 'view_' + permission_to

    groups = UserGroups.objects.values('group_id').filter(user_id=user.id).all()

    for g in groups:
        user_permissions = GroupPermissions.objects.values('permission_id').filter(group_id=g['group_id']).all()

        for p in user_permissions:
            if p['permission_id'] == required_permission:
                return True

    return False

# Permissions
class BasePermission(permissions.BasePermission):
    message = 'You do not have permission to perform this action'
    permission_to = None

    def has_permission(self, request, view):
        return check_permission(request.user, request.method, self.permission_to)

class EmployeePermission(BasePermission):
    permission_to = 'employee'

class GroupsPermission(BasePermission):
    permission_to = 'group'

class GroupPermissionsPermission(BasePermission):
    permission_to = 'group_permission'

class TaskPermission(BasePermission):
    permission_to = 'task'
