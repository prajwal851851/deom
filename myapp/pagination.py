from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class blogcursorPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'
    