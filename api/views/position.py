from api.serializers import PositionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
#from rest_framework.parsers import JSONParser

from django.utils.datastructures import MultiValueDictKeyError

from tracker.models import User, Position


class UserPositionManager(APIView):
    """
    Manage incoming (GET, POST) requests and save to DB
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
        Add position of a user to DB
        """
        try:
            if not User.exists(request.data['user']):
                pk = request.data['user']
                error = {
                    'user': ErrorDetail(string=f"Invalid pk '{pk}' - object does not exist",
                                        code='does_not_exist')
                }
                return Response(error, status=status.HTTP_404_NOT_FOUND)

        except MultiValueDictKeyError:
            error = {
                'user': ErrorDetail(string="This field is required", code='required')
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = PositionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPositionDetails(APIView):
    """
    Show position of a user
    """

    def get_last_position(self, user_id):
        positions = Position.objects.filter(user_id=user_id)
        if positions.exists():
            return positions[len(positions)-1]
        return None

    def get(self, request, pk):
        position = self.get_last_position(pk)
        if position:
            serializer = PositionSerializer(position)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GroupPositionDetails(APIView):
    """
    Return position of a group
    """

    def get(self, request):
        return Response(status=status.HTTP_510_NOT_IMPLEMENTED)

