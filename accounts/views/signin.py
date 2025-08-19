from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from accounts.views.base import Base

class Signin(Base):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(email, password)

        token = RefreshToken.for_user(user)

        enterprise = self.get_enterprise_user(user.id)

        serializer = UserSerializer(enterprise)

        return Response({
            'user': serializer.data,
            'enterprise': enterprise,
            'refresh': str(token),
            'access': str(token.access_token),
        })
