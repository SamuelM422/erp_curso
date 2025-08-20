from rest_framework import serializers
from companies.models import Employee, Task
from accounts.models import UserGroups, Group, GroupPermissions
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

class EmployeesSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email'
        )

    @staticmethod
    def get_name(obj):
        return obj.user.name

    @staticmethod
    def get_email(obj):
        return obj.user.email

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'email',
            'groups'
        )

    @staticmethod
    def get_name(obj):
        return obj.user.name

    @staticmethod
    def get_email(obj):
        return obj.user.email

    @staticmethod
    def get_groups(obj):
        groups_db = UserGroups.objects.filter(user_id=obj.user.id).all()
        groups_data = []

        for g in groups_db:
            groups_data.append({
                'id': g.group.id,
                'name': g.group.name,
            })

        return groups_data

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions'
        )

    @staticmethod
    def get_permissions(obj):
        permissions_db = GroupPermissions.objects.filter(group_id=obj.id).all()
        permissions_data = []

        for p in permissions_db:
            permissions_data.append({
                'id': p.permission.id,
                'label': p.permission.name,
                'codename': p.permission.codename
            })

        return permissions_data