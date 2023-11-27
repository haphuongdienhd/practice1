from abc import ABC

from django.http import Http404, HttpResponse, HttpResponseNotFound

from rest_framework import status

class ExceptionNotFound(Exception):
    pass

class ExceptionAlreadyExists(Exception):
    pass

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
    """Return 404 Response"""
    def __init__(self, object: Object, id: int):
        self.object = object
        self.id = id

    def __str__(self):
        return f"{str(self.object)} with id {self.id} does not exist"
    
class ObjectNotFoundByName(ExceptionNotFound):
    """Return 404 Response"""
    def __init__(self, object: Object, name: str):
        self.object = object
        self.name = name

    def __str__(self):
        return f"{str(self.object)} with name {self.name} does not exist"
    
class ObjectWithNameExists(ExceptionAlreadyExists):
    """Return 404 Response"""
    def __init__(self, object: Object, name: str):
        self.object = object
        self.name = name

    def __str__(self):
        return f"{str(self.object)} with name {self.name} already exists"