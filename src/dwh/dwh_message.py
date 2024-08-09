import json
import uuid
from typing import Any

from UUIDEncoder import UUIDEncoder
from action_dwh_enum import ActionDWHEnum


class DwhMessage:
    """
    Class for describing message, which will be sent to dwh service during MQ
    """

    def __init__(self, object_type: str, object: Any, description: str, action: ActionDWHEnum) -> None:
        """
        Create a dwh message
        :param object_type: Type of object
        :param object: object itself
        :return None:
        """
        self.object_type: str = object_type
        self.object: Any = object
        self.description: str = description
        self.action: ActionDWHEnum = action

    def get_object(self):
        return self.object

    def get_object_type(self):
        return self.object_type

    def to_dict(self):
        dwh_message_dict = dict()
        dwh_message_dict['object_type'] = self.object_type
        dwh_message_dict['description'] = self.description
        dwh_message_dict['action'] = self.action.value
        if isinstance(self.object, dict):
            obj_dict = self.object
        elif isinstance(self.object, str):
            obj_dict = str(self.object)
        else:
            obj_dict = self.object.as_dict()
        dwh_message_dict['object'] = json.dumps(obj_dict, cls=UUIDEncoder)
        return dwh_message_dict

    def __str__(self):
        return json.dumps(self.to_dict(), cls=UUIDEncoder)