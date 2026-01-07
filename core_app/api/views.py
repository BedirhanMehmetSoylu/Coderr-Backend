from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_app.models import UserProfile
from offers_app.models import Offer
from reviews_app.models import Review
from django.db.models import Avg


class BaseInfoView(APIView):
    """
    API endpoint to retrieve basic platform statistics.

    This view provides general information about the platform, including:
    - Total number of reviews
    - Average rating across all reviews (rounded to 1 decimal)
    - Number of business user profiles
    - Number of offers

    No authentication or permissions are required to access this endpoint.

    URL:
        GET /api/base-info/

    Response Example:
    {
        "review_count": 10,
        "average_rating": 4.6,
        "business_profile_count": 45,
        "offer_count": 150
    }

    Status Codes:
        200: Successfully retrieved statistics
        500: Internal server error
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        """
        Handle GET requests to fetch platform statistics.

        Steps:
        1. Count all reviews in the system.
        2. Calculate the average rating across all reviews.
        3. Count all business user profiles.
        4. Count all offers.
        5. Return a JSON response with the statistics.
        """
        try:
            review_count = Review.objects.count()

            average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
            average_rating = round(average_rating, 1)

            business_profile_count = UserProfile.objects.filter(user__type='business').count()

            offer_count = Offer.objects.count()

            data = {
                'review_count': review_count,
                'average_rating': average_rating,
                'business_profile_count': business_profile_count,
                'offer_count': offer_count
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
