from api.serializers import GroupSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework.parsers import JSONParser
from django.utils.datastructures import MultiValueDictKeyError


from tracker.models import User, Group, Position

class GroupManager(APIView):
    """
    Group Manager
    """

    def get(self, request):
        #import pdb; pdb.set_trace()
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)

        return Response(serializer.data)

    def post(self, request):
        #import pdb; pdb.set_trace()
        try:
            group = Group.objects.get(pk = request.data['group_id'])
            serializer = GroupSerializer(group, data = request.data)

        except Group.DoesNotExist:
            serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetails(APIView):
    """
    Show details about a group
    """

    def get(self, request, pk):

        try:
            #import pdb; pdb.set_trace()
            group = Group.objects.get(pk = pk)
            serializer = GroupSerializer(group)
            return Response(serializer.data)

        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class GroupMembers(APIView):
    """
    Manage group members (show and add members)
    """

    def get(self, request, pk):
        """
        Show all member that belong to a group
        """

        try:
            group = Group.objects.get(pk = pk)
            users = group.users.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)


        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        """
        Add a members to a group
        """
        #import pdb; pdb.set_trace()
        try:
            users = User.objects.filter(user_id__in=request.data.getlist('users'))
            group = Group.objects.get(pk = pk)
            group.users.add(*users)

            return Response(status=status.HTTP_201_CREATED)

        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        except MultiValueDictKeyError:
            raise Exception("Required field: users")
