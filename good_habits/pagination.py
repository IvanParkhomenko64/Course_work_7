from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Класс описания пагинации"""

    page_size = 10  # количество элементов на странице