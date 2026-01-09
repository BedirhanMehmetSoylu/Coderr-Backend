from rest_framework.pagination import PageNumberPagination

class OfferPagination(PageNumberPagination):
    """
    Custom pagination class for Offer listings.

    Attributes:
        page_size (int): Default number of offers per page.
        page_size_query_param (str): Query param to override page size.
    """
    page_size = 10
    page_size_query_param = "page_size"