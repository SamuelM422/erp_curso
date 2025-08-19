from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import get_user_model
from companies.models import Enterprise, Employee

User = get_user_model()

class Authentication:
    @staticmethod
    def signin(email=None, password=None):
        exception_auth = AuthenticationFailed('Email or password incorrect')
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            raise exception_auth

        user = User.objects.get(email=email)

        if not check_password(password, user.password):
            raise exception_auth

        return user

    @staticmethod
    def signup(name, email, password, type_account='owner', company_id=False):
        if not name or name == '':
            raise APIException('Name is required')

        if not email or email == '':
            raise APIException('Email is required')

        if not password or password == '':
            raise APIException('Password is required')

        if type_account == 'employee' and not company_id:
            raise APIException('Type account is required')

        if User.objects.filter(email=email).exists():
            raise APIException('Email already exists')

        password_hashed = make_password(password)

        created_user = User.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=type_account == 'owner'
        )

        if type_account == 'owner':
            Enterprise.objects.create(
                name='Enterprise name',
                owner_id=created_user.pk
            )

        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id,
                user_id=created_user.pk
            )

        return created_user