from django.test import (
    TestCase,
    Client
)
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from tracker.models import User, Position, Group


class TestGroupManagerView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_missed_group_id(self):
        data = {
            # missed group_id parameter
        }


        r = self.client.post('/api/group/', data=data)
        #import pdb; pdb.set_trace()
        expected = {
                'group_id': ErrorDetail(string="This field is required",
                                        code='required')
            }

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data, expected)

    def test_new_group(self):
        pk = 'G000001A'
        data = {
            'group_id': pk, # group does not exist
            'name': f'group-{pk}',
        }

        r = self.client.post('/api/group/', data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        group = self.client.get(f"/api/group/{pk}/")
        self.assertEqual(group.status_code, status.HTTP_200_OK)

        self.assertEqual(r.data, group.data)


    def test_update_group_data(self):
        pk = 'G000001B'
        data = {
            'group_id': pk, # group does not exist
            'name': f'group-{pk}',
        }

        r = self.client.post('/api/group/', data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)


        update_data = {
            'group_id': pk,
            'name': f'G-{pk}',
            'users': []
        }

        r = self.client.post('/api/group/', data=update_data)
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        group = self.client.get(f'/api/group/{pk}/')
        self.assertEqual(group.data, update_data)


class TestGroupDetailsView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_group_not_exist(self):
        pk = 'G000001C' # group does not exist

        r = self.client.get(f'/api/group/{pk}/')

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_details(self):

        pk = "G000001D"
        group_data = {
            'group_id': pk,
            'name': f'group-{pk}',
            'users': []
        }

        r = self.client.post('/api/group/', data=group_data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        group = self.client.get(f'/api/group/{pk}/')

        self.assertEqual(group.status_code, status.HTTP_200_OK)
        self.assertEqual(group.data, group_data)


class TestGroupMembersView(TestCase):
    def setUp(self):
        self.client = Client()

        # creating users
        self.users = ["U00000A", "U00000B"]
        for user_pk in self.users:
            r = self.client.post('/api/user/',
                                 data={'user_id': user_pk,
                                       'name':f'user-{user_pk}'})
            self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_group_not_exist(self):
        pk = "G000001E" # group does not exist

        r = self.client.get(f'/api/group/{pk}/')

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_users2group_not_exist(self):
        ## adding members to a group that does not exist
        pk = "G000001Z"

        r = self.client.post(f'/api/group/{pk}/members/',
                             data={'users':self.users})

        expected = {
                'group': ErrorDetail(string=f"Invalid pk '{pk}' - group does not exist",
                                     code='does_not_exist')
        }

        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.data, expected)

    def test_missed_users_parameter(self):
        ## creating group
        pk = "G000001Z"
        data = {
            'group_id': pk, # group does not exist
            'name': f'group-{pk}',
        }

        r = self.client.post('/api/group/', data=data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        ## adding member (but forgot pass users parameter)
        r = self.client.post(f'/api/group/{pk}/members/', data={})

        expected = {
            'users': ErrorDetail(string="This field is required",
                                 code='required')
        }

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.data, expected)


    def test_add_users2group(self):
        group_pk = "G000001G"
        group_data = {
            'group_id': group_pk,
            'name': f'group-{group_pk}',
        }

        r = self.client.post('/api/group/', data=group_data)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        r = self.client.post(f'/api/group/{group_pk}/members/',
                             data={'users':self.users})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        #import pdb; pdb.set_trace()
        users = self.client.get(f'/api/group/{group_pk}/members/')
        users_ids = [user['user_id'] for user in users.data]

        self.assertEqual(users_ids, self.users)
