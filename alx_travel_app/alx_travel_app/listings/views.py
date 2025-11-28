"""API endpoints for listings-related functionality."""

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Simple endpoint to verify that the service is responding."""

    def get(self, request):
        return Response({"status": "ok"})
