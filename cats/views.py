from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
# from rest_framework.pagination import (
#     LimitOffsetPagination,
#     PageNumberPagination
# )
from rest_framework.throttling import ScopedRateThrottle

from .models import Achievement, Cat, User
# from .pagination import CatsPagination
from .permissions import OwnerOrReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к базе котов."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    # Для любых пользователей установим кастомный лимит 1 запрос в минуту
    throttle_scope = 'low_request'
    # pagination_class = LimitOffsetPagination
    # Вот он наш собственный класс пагинации с page_size=20
    # pagination_class = CatsPagination
    # Указываем фильтрующий бэкенд DjangoFilterBackend
    # Из библиотеки django-filter
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    # Временно отключим пагинацию на уровне вьюсета,
    # так будет удобнее настраивать фильтрацию
    pagination_class = None
    # Фильтровать будем по полям color и birth_year модели Cat
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year')  # поля для сотрировки в запросе
    ordering = ('birth_year',)  # сортировка по конкретному полю по-умолчанию

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_permissions(self):
    #     # Если в GET-запросе требуется получить информацию об объекте
    #     if self.action == 'retrieve':
    #         # Вернём обновлённый перечень используемых пермишенов
    #         return (ReadOnly(),)
    #     # Для остальных ситуаций оставим текущий перечень
    #     # пермишенов без изменений
    #     return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Обрабатывает запросы к базе пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к базе котячьих ачивок."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
