from rest_framework.pagination import PageNumberPagination


class PaginacionProductos(PageNumberPagination):
    """Paginación estándar; el cliente puede pedir ?page_size=N (máx. 20)."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20