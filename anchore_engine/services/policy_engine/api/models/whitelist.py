# coding: utf-8


from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from anchore_engine.services.policy_engine.api.models.base_model_ import Model
from anchore_engine.services.policy_engine.api.models.whitelist_item import WhitelistItem  # noqa: F401,E501
from anchore_engine.services.policy_engine.api import util


class Whitelist(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, version=None, comment=None, items=None):  # noqa: E501
        """Whitelist - a model defined in Swagger

        :param id: The id of this Whitelist.  # noqa: E501
        :type id: str
        :param name: The name of this Whitelist.  # noqa: E501
        :type name: str
        :param version: The version of this Whitelist.  # noqa: E501
        :type version: str
        :param comment: The comment of this Whitelist.  # noqa: E501
        :type comment: str
        :param items: The items of this Whitelist.  # noqa: E501
        :type items: List[WhitelistItem]
        """
        self.swagger_types = {
            'id': str,
            'name': str,
            'version': str,
            'comment': str,
            'items': List[WhitelistItem]
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version',
            'comment': 'comment',
            'items': 'items'
        }

        self._id = id
        self._name = name
        self._version = version
        self._comment = comment
        self._items = items

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Whitelist of this Whitelist.  # noqa: E501
        :rtype: Whitelist
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Whitelist.


        :return: The id of this Whitelist.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Whitelist.


        :param id: The id of this Whitelist.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this Whitelist.


        :return: The name of this Whitelist.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Whitelist.


        :param name: The name of this Whitelist.
        :type name: str
        """

        self._name = name

    @property
    def version(self):
        """Gets the version of this Whitelist.


        :return: The version of this Whitelist.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Whitelist.


        :param version: The version of this Whitelist.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def comment(self):
        """Gets the comment of this Whitelist.


        :return: The comment of this Whitelist.
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this Whitelist.


        :param comment: The comment of this Whitelist.
        :type comment: str
        """

        self._comment = comment

    @property
    def items(self):
        """Gets the items of this Whitelist.


        :return: The items of this Whitelist.
        :rtype: List[WhitelistItem]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this Whitelist.


        :param items: The items of this Whitelist.
        :type items: List[WhitelistItem]
        """

        self._items = items