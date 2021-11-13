from api.serializers import PositionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.parsers import JSONParser

from tracker.models import User, Position


class PositionManager(APIView):
    """
    Manage incoming request and save to DB
    """

    def get(self, request):
        """
        List all position stores in DB
        """
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        Add position of a user to the DB
        """
        import pdb; pdb.set_trace()
        user =  User.objects.filter(pk=request.data['user'])
        if not user.exists():
            User.objects.create(user_id=request.data['user'])

        serializer = PositionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
