from api.serializers import PositionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tracker.models import User, Position

class PositionDetail(APIView):
    """
    Show position of a user
    """

    def get_last_position(self, user_id):
        positions = Position.objects.filter(user_id=user_id)
        
        if positions.exists():
            return positions[len(positions)-1]
        return None

    def get(self, request, pk):
        
        #try:
            #user = User.objects.get(user_id = pk)
            #import pdb; pdb.set_trace()
        position = self.get_last_position(pk)
        if position:
            serializer = PositionSerializer(position)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
       #except Exception as :
       #     raise Http404
