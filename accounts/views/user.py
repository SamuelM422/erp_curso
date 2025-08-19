from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from accounts.views.base import Base

User = get_user_model()

class GetUser(Base):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first()

        enterprise = self.get_enterprise_user(request.user.id)

        serializer = UserSerializer(user)

        return Response({
            'user': serializer.data,
            'enterprise': enterprise,
        })