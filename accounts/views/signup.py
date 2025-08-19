from rest_framework.response import Response
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from accounts.views.base import Base

class Signup(Base):
    @staticmethod
    def post(request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signup(name, email, password)

        serializer = UserSerializer(user)

        return Response(serializer.data)