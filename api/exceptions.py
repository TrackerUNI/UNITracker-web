from rest_framework.exceptions import APIException
from rest_framework import status


class UserExistsError(APIException):
    pass


class RequiredFieldError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Required field was not supplied'
    default_code = 'required_field_unavailable'
