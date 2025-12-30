from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles_app.models import UserProfile
from django.db.models import Avg

class BaseInfoView(APIView):
    permission_classes = []

    authentication_classes = []

    def get(self, request):
        try:
            review_count = 0
            average_rating = 0
            business_profile_count = UserProfile.objects.filter(user__type='business').count()
            offer_count = 0

            data = {
                'review_count': review_count,
                'average_rating': round(average_rating, 1),
                'business_profile_count': business_profile_count,
                'offer_count': offer_count
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
