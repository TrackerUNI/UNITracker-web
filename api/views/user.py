from api.serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import ErrorDetail
from django.utils.datastructures import MultiValueDictKeyError



from tracker.models import User

class UserManager(APIView):
    """
    Manage user
    """

    def get(self, request):
        #import pdb; pdb.set_trace()
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        new_user = False
        try:
            user = User.objects.get(pk = request.data['user_id'])
            serializer = UserSerializer(user, data = request.data)

        except MultiValueDictKeyError:
            error = {
                'user_id': ErrorDetail(string="This field is required", code='required')
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            new_user = True

        if serializer.is_valid():
            serializer.save()
            if new_user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    """
    Show details about a user
    """

    def get(self, request, pk):

        try:
            user = User.objects.get(pk = pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
