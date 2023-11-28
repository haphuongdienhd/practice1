from abc import ABC

from django.http import HttpResponseBadRequest, HttpResponseNotFound

from rest_framework import status
from rest_framework.response import Response

class ExceptionNotFound(Exception):
    def return_404_http(self, msg):
        return HttpResponseNotFound(
            content=str(msg),
        )
    def return_404_response(self, msg):
        "HTTP_404_NOT_FOUND"
        return Response(
                {"exception": str(msg)},
                status=status.HTTP_404_NOT_FOUND
            )

class ExceptionAlreadyExists(Exception):
    def return_400_http(self, msg):
        return HttpResponseBadRequest(
            content=str(msg),
        )
    def return_400_response(self, msg):
        "HTTP_400_BAD_REQUEST"
        return Response(
                {"exception": str(msg)},
                status=status.HTTP_400_BAD_REQUEST
            )


class Object(ABC):
    # Return kind of object as string
    def __str__(self):
        return self.__class__.__name__
    
class TokenObject(Object):
    pass

class UserObject(Object):
    pass

class ObjectNotFound(ExceptionNotFound):
    """Return 404 Message"""
    def __init__(self, object: Object, key: str, key_value):
        self.object = object
        self.key = key
        self.key_value = str(key_value)

    def __str__(self):
        return f"{str(self.object)} with {self.key} {self.key_value} does not exist"  
    
class ObjectWithKeyExists(ExceptionAlreadyExists):
    """Return 404 Message"""
    def __init__(self, object: Object, key: str, key_value):
        self.object = object
        self.key = key
        self.key_value = str(key_value)

    def __str__(self):
        return f"{str(self.object)} with {self.key} {self.key_value} already exists"