from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from .models import User
from .serializers import UserSerializer, UserRegisterSerializer
from .permissions import UserPermissions
from rest_framework.response import Response

class UserAPIViewSet(GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [UserPermissions()]
        return [AllowAny()]  # Обеспечиваем доступ всем для создания пользователя

    def perform_update(self, serializer):
        # Сохранение обновленного пользователя
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Создание нового пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Сохранение пользователя
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
