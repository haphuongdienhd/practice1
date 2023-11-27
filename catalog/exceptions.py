from abc import ABC

from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from rest_framework import status
from rest_framework.response import Response

class ExceptionNotFound(Exception):
    def return_for_web(self, msg):
        return HttpResponseNotFound(
            content=str(msg),
        )
    def return_for_api(self, msg):
        "HTTP_404_NOT_FOUND"
        return Response(
                {"exception": str(msg)},
                status=status.HTTP_404_NOT_FOUND
            )

class ExceptionAlreadyExists(Exception):
    def return_for_web(self, msg):
        return HttpResponseBadRequest(
            content=str(msg),
        )
    def return_for_api(self, msg):
        "HTTP_400_BAD_REQUEST"
        return Response(
                {"exception": str(msg)},
                status=status.HTTP_400_BAD_REQUEST
            )


class Object(ABC):
    # Return kind of object as string
    def __str__(self):
        return self.__class__.__name__
    
class ProductObject(Object):
    pass

class CategoryObject(Object):
    pass

class ProductCategoryObject(Object):
    pass

class ObjectNotFoundById(ExceptionNotFound):
    """Return 404 Message"""
    def __init__(self, object: Object, id: int):
        self.object = object
        self.id = id

    def __str__(self):
        return f"{str(self.object)} with id {self.id} does not exist"
    
    
class ObjectNotFoundByName(ExceptionNotFound):
    """Return 404 Message"""
    def __init__(self, object: Object, name: str):
        self.object = object
        self.name = name

    def __str__(self):
        return f"{str(self.object)} with name {self.name} does not exist"
    
class ObjectWithNameExists(ExceptionAlreadyExists):
    """Return 404 Message"""
    def __init__(self, object: Object, name: str):
        self.object = object
        self.name = name

    def __str__(self):
        return f"{str(self.object)} with name {self.name} already exists"