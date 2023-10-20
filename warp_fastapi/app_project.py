from __future__ import annotations

from .app_object import AppObject, AuthObject
from .base import TemplateModel


class AppProject(TemplateModel):
    """
    A class that represents an app project.

    Attributes:
        name: str: The name of the model. Name should be snake_case. From TemplateModel
        auth_object: AuthObject | None: Object that is used as authorization
        app_objects: list[AppObject]: The list of app objects in the project.
    """

    app_objects: list[AppObject]
    auth_object: AuthObject | None = None

    def __init__(self, name: str, *args: AppObject, auth_object: AuthObject | None = None):
        """
        Initialize the project with the given name and app objects.

        Args:
            name: The name of the project.
            args: AppObject: A list of app objects for the project.
            auth_object: AuthObject|None: Authorization object.
        """
        if auth_object:
            if auth_object not in args:
                args = args + (auth_object,)
        else:
            for app_obj in args:
                if app_obj.secure:
                    raise Exception("App Object can't be secure without Authenication Object")

        super().__init__(name=name, app_objects=args, auth_object=auth_object)
